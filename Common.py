import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# データベース接続パラメータ
params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

# PostgreSQLデータベースへの接続を取得する関数
def get_db_connection():
    conn = psycopg2.connect(**params)
    return conn

# 環境変数から設定を読み込む
load_dotenv()

# Azure OpenAIのクライアントを設定
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # APIキー
    api_version=os.getenv("VERSION"),  # APIのバージョン
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")  # Azure OpenAIのエンドポイント
)

def text2vector(text):
    try:
        # テキストをベクトルに変換
        vector = client.embeddings.create(
            input=text,  # 変換するテキスト
            model=os.getenv("EMBEDDING")  # 使用するモデルの環境変数名
        ).data[0].embedding
        
        # SQLに埋め込むベクトルを文字列に変換
        vector_str = str(vector)
        
        return vector_str

    except Exception as e:
        return str(e)

def search_similar_vector(vector_str):
    try:
        # データベースに接続
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # カーソルの作成
        cur = conn.cursor()

        # データの読み取り
        cur.execute("""
            SELECT knowledge_id, 1 - (%s <=> knowledge_vector) AS cosine_similarity, knowledge_text 
            FROM knowledge
            ORDER BY cosine_similarity DESC;
            """, (vector_str,))
        
        # 結果を取得
        first_row = cur.fetchone()
        
        id = str(first_row[0]) 
        similarity = str(first_row[1])
        text = str(first_row[2])
        
        # カーソルとコネクションのクローズ
        cur.close()
        conn.close()
        
        return id, similarity, text
        
    except Exception as e:
        return str(e)
        
def LLM_chat(prompt):
    try:
        # 生成AIによる回答の生成
        response = client.chat.completions.create(
            model=os.getenv("DEPLOYMENT_NAME"),  # 環境変数からモデル名を取得
            messages=[
                # システムに日本語で丁寧な回答を生成するよう指示
                {"role": "system", "content": "You generate polite answers based on the user's query. You will also need to answer in Japanese."},
                # 生成したプロンプトを設定
                {"role": "user", "content": prompt}
            ],
            # 回答の多様性を制御するパラメータの設定
            temperature=0.7
        )    
        return response.choices[0].message.content
    
    except Exception as e:
        return str(e)

def insert_data(prompt, answer):
    try:
        # データベースに接続
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # カーソルの作成
        cur = conn.cursor()

        # データの登録
        cur.execute("INSERT INTO qa (qa_prompt, qa_answer) VALUES (%s, %s)", (prompt, answer))
        
        # カーソルとコネクションのクローズ
        cur.close()
        conn.close()
    
    except Exception as e:
        return str(e)

# デバッグ用
# vector = text2vector("Hello, how are you?")
# print(vector)

# id, similarity, text = search_similar_vector(vector)
# print(f"id: {id}, similarity: {similarity}, text: {text}")

# insert_data("aaaa", "aaaa")

# response = LLM_chat(text)
# print(response)

