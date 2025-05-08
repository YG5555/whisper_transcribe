import whisper
import os

def run_transcription(audio_file_path: str) -> tuple[dict, str]:
    print("受け取ったパス:", audio_file_path)
    print("ファイル存在確認:", os.path.exists(audio_file_path))  # ← ここ追加

    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)

    text_result = result.get("text", "")
    return result, text_result