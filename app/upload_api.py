from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.transcriber import run_transcription

import os

router = APIRouter()

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # 一時パスへ保存
        tmp_path = f"/tmp/{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        # 文字起こし実行
        output_json, output_txt = run_transcription(audio_file_path=tmp_path)

        return JSONResponse(content={
            "status": "success",
            "json_result": output_json,
            "text_result": output_txt
        })

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"ファイルが見つかりません: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラー: {e}")