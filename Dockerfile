# 1. ベースはPython 3.10
FROM python:3.10

# 【ここが修正ポイント！】
# 音声ファイルを扱うための必須ツール「ffmpeg」をインストールします
# これがないとWhisperが動きません
RUN apt-get update && apt-get install -y ffmpeg

# 2. 作業場所を確保
WORKDIR /code

# 3. 権限設定（エラー回避のお守り）
# データの読み書き権限トラブルを防ぐため、フォルダの権限を広げておきます
RUN chmod -R 777 /code

# 4. 材料リストをコピーしてインストール
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. すべてのファイルをコピー
COPY . /code

# 6. アプリ起動（ポート7860）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]