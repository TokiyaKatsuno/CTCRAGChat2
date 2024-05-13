# ファイルパスからファイルデータの内容を読み込む
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# データの定義
file_url_data = {
    "PGVector/下請法_登録データ/第4条第1項第2号_法文.txt" : "https://www.jftc.go.jp/shitauke/legislation/act.html",
    "PGVector/下請法_登録データ/第4条第1項第2号_運用基準.txt": "https://www.jftc.go.jp/shitauke/legislation/unyou.html",
    "PGVector/下請法_登録データ/第4条第1項第2号_運用基準_事例.txt": "https://www.jftc.go.jp/shitauke/legislation/unyou.html",
    "PGVector/下請法_登録データ/第3条_法文.txt": "https://www.jftc.go.jp/shitauke/legislation/act.html",
    "PGVector/下請法_登録データ/第3条_運用基準_1.txt": "https://www.jftc.go.jp/shitauke/legislation/unyou.html",
    "PGVector/下請法_登録データ/第3条_運用基準_2.txt": "https://www.jftc.go.jp/shitauke/legislation/unyou.html",
    "PGVector/下請法_登録データ/第3条_運用基準_3.txt": "https://www.jftc.go.jp/shitauke/legislation/unyou.html"
}




# 必要なライブラリのインポート
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 環境変数から設定を読み込む
load_dotenv()

# Azure OpenAIのクライアントを設定
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # APIキー
    api_version=os.getenv("VERSION"),  # APIのバージョン
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")  # Azure OpenAIのエンドポイント
)

# データベース接続パラメータ
params = {
    "host": "127.0.0.1",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

# リストのテキストとURLデータをデータベースに入れる
for file_path, url in file_url_data.items():
    print(file_path)
    print(url)
    
    # データのテキストと情報源の設定
    law_text = read_file_content(file_path)
    law_source = url
    
    # ユーザーに入力したテキストを確認させる
    print(f"【STEP0】 あなたの入力したテキストは以下ですね。\n{law_text}\n")

    # テキストをベクトルに変換
    law_vector = client.embeddings.create(
        input=law_text,  # 変換するテキスト
        model=os.getenv("EMBEDDING")  # 使用するモデルの環境変数名
    ).data[0].embedding

    # ベクトルの長さ（次元数）を計算
    len_vector = len(law_vector)  # `len`を変数名として使用すると、組み込み関数`len()`を上書きしてしまうため、`len_vector`としています
    print(len_vector)
    print(law_vector)

    # データベースに接続
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # カーソルの作成
    cur = conn.cursor()

    # knowledgeテーブル,qaテーブルの作成
    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
        knowledge_id BIGSERIAL PRIMARY KEY, 
        knowledge_text VARCHAR(100000),
        knowledge_vector VECTOR(1536), 
        knowledge_source VARCHAR(1000)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS qa (
        qa_id BIGSERIAL PRIMARY KEY, 
        qa_prompt VARCHAR(100000),
        qa_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        qa_answer VARCHAR(100000),
        qa_modified_answer VARCHAR(100000),
        qa_bleu DOUBLE PRECISION
        )
    """)


    # データの挿入
    cur.execute("INSERT INTO knowledge (knowledge_text, knowledge_vector, knowledge_source) VALUES (%s, %s, %s)", (law_text, law_vector, law_source))

# データの読み取り
cur.execute("SELECT * FROM knowledge;")
rows = cur.fetchall()
for row in rows:
    print(row)

# カーソルとコネクションのクローズ
cur.close()
conn.close()
