#FastAPI起動用

from fastapi import FastAPI
from app.upload_api import router as upload_router

app = FastAPI()
app.include_router(upload_router)