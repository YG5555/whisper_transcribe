from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.transcriber_core import run_transcription

router = APIRouter()

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        temp_file_path = f"/tmp/{file.filename}"
        file.file.seek(0)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if not os.path.exists(temp_file_path):
            return {"error": f"保存に失敗: {temp_file_path} が存在しません"}

        json_result, text_result = run_transcription(temp_file_path)
        os.remove(temp_file_path)

        return {
            "text": text_result,
            "raw": json_result
        }

    except FileNotFoundError:
        return {"error": "ファイルが見つかりませんでした"}
    except Exception as e:
        return {"error": str(e)}