import os
from pathlib import Path
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# --- APIルーターのインポート ---
# 各種機能（アップロード、文字起こし等）を呼び出すための設定です
from app.api import transcribe_api, upload_api, health_api, result_api, status_api, download_api

app = FastAPI(title="Whisper Transcribe API", version="1.0.0")

# --- 1. CORS設定の修正（最重要） ---
# フロントエンド（React）からの接続を許可するための設定です。
# Hugging FaceのURLを許可リストに追加しました。
origins = [
    "https://whisper-transcribe-mdxq.onrender.com",  # 以前のRender用（念のため残しています）
    "https://yg5555-whisper.hf.space",               # ★修正：Hugging FaceのアプリURLを追加
    "https://yg5555-whisper.hf.space/",              # ★念のため、末尾にスラッシュがある版も追加
    "http://localhost:3000",                        # ローカル開発用
    "http://127.0.0.1:3000",                      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. APIルーターの登録 ---
# アプリの各窓口（URL）を登録しています
app.include_router(transcribe_api.router, prefix="/api", tags=["transcribe"])
app.include_router(upload_api.router, prefix="/api", tags=["upload"])
app.include_router(health_api.router, prefix="/api", tags=["health"])
app.include_router(result_api.router, prefix="/api", tags=["result"])
app.include_router(status_api.router, prefix="/api", tags=["status"])
app.include_router(download_api.router, prefix="/api", tags=["download"])

# --- 3. 静的ファイル（Reactアプリ）の配信設定 ---
# 画面（UI）を表示するための設定です。
frontend_build_path = Path("./static")

if frontend_build_path.exists():
    # 画面を表示するための「static」フォルダがある場合の処理です
    app.mount(
        "/", 
        StaticFiles(directory=str(frontend_build_path), html=True), 
        name="static-root"
    )
else:
    # フォルダが見つからない場合の予備メッセージです
    @app.get("/")
    async def root_fallback():
        return {
            "message": "Whisper Transcribe API is running on Hugging Face", 
            "error": "Frontend static directory not found.",
            "path_checked": str(frontend_build_path.resolve())
        }

# --- 4. サーバー起動設定（Hugging Face対応） ---
if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spacesの標準ポート番号は「7860」です。
    # 環境変数 PORT が設定されていない場合は 7860 を使うように設定しました。
    port = int(os.getenv("PORT", 7860))
    
    # アプリを起動します。
    # フォルダ構造に合わせて "app.main:app" と指定します。
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)