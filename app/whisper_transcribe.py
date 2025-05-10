# 仮想環境のPythonを指定
#!/Users/yg/projects/whisper_diarization/whisper_env/bin/python

# SSL認証を無効化（必要に応じて使用）
#SSLの認証
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import glob
import whisper
import json
import shutil

from app.core.transcriber import run_transcription_basic as run_transcription

# FastAPIの構成要素や外部UI、ルーターをインポート
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.gradio_ui import transcribe_gradio_ui
import gradio as gr
from app.upload_api import router as upload_router

# FastAPIアプリケーションを作成
app = FastAPI()

app.include_router(upload_router, prefix="/api")

# Gradio UIアプリを生成
gradio_app = transcribe_gradio_ui()
app = gr.mount_gradio_app(app, gradio_app, path="/")

# API経由で文字起こしを行うエンドポイント
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

if __name__ == "__main__":
    output_path = run_transcription()
    print(f"文字起こし完了: {output_path}")