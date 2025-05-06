import gradio as gr
from whisper_transcribe import run_transcription
import shutil
import time

status_textbox = None

def transcribe_with_status(filepath):
    global status_textbox
    if status_textbox is not None:
        status_textbox.update(value="ステータス: 音声ファイルをコピー中...")
    shutil.copy(filepath, "../audio/input_audio.wav")
    time.sleep(0.5)

    if status_textbox is not None:
        status_textbox.update(value="ステータス: Whisperで文字起こし中...")
    _, text_path = run_transcription()

    if status_textbox is not None:
        status_textbox.update(value="ステータス: 完了しました。")
    with open(text_path, "r", encoding="utf-8") as f:
        return f.read()

def transcribe_gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# Whisper 文字起こしアプリ")
        audio_input = gr.Audio(type="filepath", label="音声ファイルを選択")
        global status_textbox
        status_textbox = gr.Textbox(label="進捗ステータス", interactive=False)
        result_text = gr.Textbox(label="文字起こし結果", lines=10)
        btn = gr.Button("実行")

        btn.click(fn=transcribe_with_status, inputs=audio_input, outputs=result_text)
    return demo