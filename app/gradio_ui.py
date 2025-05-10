# Gradioライブラリをインポート（UI構築用）
import gradio as gr
# 文字起こし処理を行う関数をインポート
from app.whisper_transcribe import run_transcription
# ファイル操作用モジュールをインポート
import shutil
# 処理の待機時間を挿入するためのモジュールをインポート
import time

status_textbox = None

# 音声ファイルの文字起こしを実行し、ステータスを表示
def transcribe_with_status(filepath):
    global status_textbox
    if status_textbox is not None:
        status_textbox.update(value="ステータス: 音声ファイルをコピー中...")
    # ファイルを所定のパスにコピー
    shutil.copy(filepath, "../audio/input_audio.wav")
    # 少し待ってから次の処理へ
    time.sleep(0.5)

    if status_textbox is not None:
        status_textbox.update(value="ステータス: Whisperで文字起こし中...")
    _, text_path = run_transcription()

    if status_textbox is not None:
        status_textbox.update(value="ステータス: 完了しました。")
    # 結果ファイルを読み込んで内容を返す
    with open(text_path, "r", encoding="utf-8") as f:
        return f.read()

# Gradio UIの構築
def transcribe_gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# Whisper 文字起こしアプリ")
        audio_input = gr.Audio(type="filepath", label="音声ファイルを選択")
        global status_textbox
        status_textbox = gr.Textbox(label="進捗ステータス", interactive=False)
        result_text = gr.Textbox(label="文字起こし結果", lines=10)
        btn = gr.Button("実行")

        # ボタンがクリックされたときに文字起こし関数を実行
        btn.click(fn=transcribe_with_status, inputs=audio_input, outputs=result_text)
    return demo