# 1. Python 3.10環境をベースにします
FROM python:3.10

# 2. コンテナ内での作業ディレクトリ（作業場所）を /code に設定します
WORKDIR /code

# 3. 材料リストをコピーしてライブラリをインストールします
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. 全てのファイルをコンテナにコピーします（app/ フォルダも含まれます）
COPY . /code

# 5. Hugging Face専用ポート7860でアプリを起動します
# 注意: プログラムが app/main.py にあるため、"app.main:app" と指定します
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]