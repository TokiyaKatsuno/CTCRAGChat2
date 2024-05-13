# テキストの設定
text = "遅延" 
#text = "ABSが作動しない"

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
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

# ユーザーに入力したテキストを確認させる
print(f"【STEP0】 あなたの入力したテキストは以下ですね。\n{text}\n")

# テキストをベクトルに変換
vector = client.embeddings.create(
    input=text,  # 変換するテキスト
    model=os.getenv("EMBEDDING")  # 使用するモデルの環境変数名
).data[0].embedding

# データベースに接続
conn = psycopg2.connect(**params)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# カーソルの作成
cur = conn.cursor()

# SQLに埋め込むベクトルを文字列に変換
vector_str = str(vector)

# 検索結果を出力
print(f"【STEP1】ベクトル検索の結果、類似度が高かった順に表示します。")

# データの読み取り
cur.execute("""
    SELECT knowledge_id, 1 - (%s <=> knowledge_vector) AS cosine_similarity, knowledge_text 
        FROM knowledge
        ORDER BY cosine_similarity DESC;
        """, (vector_str,))
rows = cur.fetchall()
for row in rows:
    print(row)

# カーソルとコネクションのクローズ
cur.close()
conn.close()
