import os
import shutil
import datetime
import glob
import whisper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
ARCHIVE_DIR = os.path.join(BASE_DIR, "audio_archive")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def run_transcription_basic():
    # 出力ディレクトリとアーカイブディレクトリが存在しない場合は作成する
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # 音声ファイルの一覧を取得し、更新日時の降順でソートする
    audio_files = sorted(
        glob.glob(os.path.join(AUDIO_DIR, "*.*")),
        key=os.path.getmtime,
        reverse=True
    )

    # 音声ファイルが存在しない場合は処理を終了する
    if not audio_files:
        print("音声ファイルがありません。")
        return

    # 最新の音声ファイルを取得し、処理対象として表示する
    audio_path = audio_files[0]
    print(f"文字起こし対象ファイル: {audio_path}")

    # Whisperモデルをロードし、音声ファイルの文字起こしを実行する
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    # 現在の日時を取得し、結果ファイルの名前に付加する
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.splitext(os.path.basename(audio_path))[0] + f"_{timestamp}.txt"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # 文字起こし結果をテキストファイルとして保存する
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"文字起こし結果を保存しました: {output_path}")

    # 処理済みの音声ファイルをアーカイブディレクトリに移動する
    shutil.move(audio_path, os.path.join(ARCHIVE_DIR, os.path.basename(audio_path)))
    print(f"元ファイルをアーカイブに移動しました。")