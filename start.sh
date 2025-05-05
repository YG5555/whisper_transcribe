#!/bin/bash
uvicorn app.whisper_transcribe:app --host=0.0.0.0 --port=10000