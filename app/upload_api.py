# FastAPIの必要なモジュールをインポート
from fastapi import APIRouter, UploadFile, File, HTTPException
# レスポンス形式としてJSONを使用
from fastapi.responses import JSONResponse
# 音声文字起こしの関数をインポート
from app.core.transcriber import run_transcription_basic

import os

# ルーターを作成（APIエンドポイントの定義に使用）
router = APIRouter()

# 音声ファイルをアップロードして文字起こしを実行するエンドポイント
@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # アップロードされたファイルを一時保存するパスを定義
        tmp_path = f"/tmp/{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        # 文字起こし処理を実行し、結果を取得
        output_json, output_txt = run_transcription_basic(audio_file_path=tmp_path)

        # 成功レスポンスとして結果をJSON形式で返す
        return JSONResponse(content={
            "status": "success",
            "json_result": output_json,
            "text_result": output_txt
        })

    # ファイルが見つからなかった場合の例外処理
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"ファイルが見つかりません: {e}")
    # その他の例外を処理
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラー: {e}")