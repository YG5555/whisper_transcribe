#文字起こしのみ

#仮想環境
#!/Users/yg/projects/whisper_diarization/whisper_env/bin/python

#SSLの認証
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import glob
import whisper
import json
import shutil

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.gradio_ui import transcribe_gradio_ui
import gradio as gr
from app.transcriber_core import run_transcription

def transcribe_file(file_path: str) -> tuple[dict, str]:
    return run_transcription(file_path)

#関数化
def run_transcription():
    # フォルダ設定
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AUDIO_DIR = os.path.join(BASE_DIR, "audio")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    AUDIO_ARCHIVE_DIR = os.path.join(BASE_DIR, "audio_archive")

    # 対象ファイル拡張子
    EXTENSIONS = ["*.wav", "*.mp3", "*.m4a"]

    # 音声ファイルリスト作成
    audio_files = [f for ext in EXTENSIONS for f in glob.glob(os.path.join(AUDIO_DIR, ext))]
    if not audio_files:
        raise FileNotFoundError("audioフォルダに音声ファイルがありません")

    # 最新のファイルを選択
    audio_file_path = max(audio_files, key=os.path.getmtime)

    # ファイル名取得（拡張子なし）
    file_name = os.path.splitext(os.path.basename(audio_file_path))[0]

    # Whisperモデルロード
    model = whisper.load_model("medium")

    # 文字起こし実行
    result = model.transcribe(audio_file_path, language="ja", verbose=False)

    # 出力フォルダ作成
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # JSONファイルに保存
    output_path = os.path.join(OUTPUT_DIR, f"{file_name}_result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # テキストファイルにも保存
    text_output_path = os.path.join(OUTPUT_DIR, f"{file_name}_result.txt")
    with open(text_output_path, "w", encoding="utf-8") as f:
        # まず元ファイル名を書く
        f.write(f"[元ファイル名: {file_name}]\n\n")
        # そのあとセグメントごとの開始・終了時刻を書く
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            f.write(f"[{start:.2f} - {end:.2f}]\n")

    # 入力音声ファイルもaudio_archiveへ移動
    os.makedirs(AUDIO_ARCHIVE_DIR, exist_ok=True)
    shutil.move(audio_file_path, os.path.join(AUDIO_ARCHIVE_DIR, os.path.basename(audio_file_path)))

    print(f"✅ 文字起こし完了: {output_path} と {text_output_path}")
    return output_path, text_output_path

if __name__ == "__main__":
    run_transcription()

app = FastAPI()

app.include_router(upload_router, prefix="/api")

gradio_app = transcribe_gradio_ui()
app = gr.mount_gradio_app(app, gradio_app, path="/")

@app.post("/transcribe")
def transcribe_api():
    try:
        output_json, output_txt = run_transcription()
        return JSONResponse(content={
            "status": "success",
            "json_result": output_json,
            "text_result": output_txt
        })
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"音声ファイルが見つかりません: {e}")
    except whisper.WhisperException as e:
        raise HTTPException(status_code=500, detail=f"Whisperエラー: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"予期しないエラー: {e}")