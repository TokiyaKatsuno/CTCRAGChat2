from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Flaskアプリケーションを初期化
app = Flask(__name__)

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

# ルートエンドポイントの作成
@app.route('/')
def index():
    return render_template('SimpleChat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'message': 'Please provide a message'}), 400
    
    try:
        # テキストをベクトルに変換
        vector = client.embeddings.create(
            input=user_input,  # 変換するテキスト
            model=os.getenv("EMBEDDING")  # 使用するモデルの環境変数名
        ).data[0].embedding
        
        # SQLに埋め込むベクトルを文字列に変換
        vector_str = str(vector)

        AIChat_response = "【STEP1】ベクトル化\n"
        AIChat_response += "テキスト:" + user_input + "\n"
        AIChat_response += "ベクトル値:" + vector_str[:91] + "...]\n\n"

        # データベースに接続
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # カーソルの作成
        cur = conn.cursor()

        # データの読み取り
        cur.execute("""
            SELECT id, 1 - (%s <=> embedding) AS cosine_similarity, text 
            FROM vectors
            ORDER BY cosine_similarity DESC;
            """, (vector_str,))
        
        # 結果を取得
        first_row = cur.fetchone()
        
        AIChat_response += "【STEP2】ベクトル検索\n"
        AIChat_response += "ID:" + str(first_row[0]) + "\n"
        AIChat_response += "類似度:" + str(first_row[1]) + "\n"
        AIChat_response += "テキスト:" + first_row[2] + "\n\n"
        
        # プロンプトの作成
        # 上記で読み込んだベクトル検索の結果を基に、詳細な指示を作成
        prompt = f"""
        ###命令
        あなたは優秀な自動車整備士です。
        「{user_input}」という症状に対する原因と行うべき対策について'###「ABSが作動しない」に対するベクトル検索の結果'を参照し、詳しく説明してください 。
        ###手順
        1. ベクトル検索の結果をもとに考えうる具体的な原因を書き出す。
        2. 1.で挙げた原因に対する具体的な対応策を書き出す。
        ###出力形式
        1-1.原因:xxxxx
        1-2.対応策:xxxxx
        ### ベクトル検索の結果
        {first_row[2]}
        """
        
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
        
        AIChat_response += "【STEP3】生成AIによる回答\n"
        AIChat_response += response.choices[0].message.content + "\n"
        
        # 改行をHTMLタグに変換
        AIChat_response_html = AIChat_response.replace("\n", "<br \>")
        
        # カーソルとコネクションのクローズ
        cur.close()
        conn.close()
        
        return jsonify({'response': AIChat_response_html}), 200
                       
    except Exception as e:
        return jsonify({'response': 'An error occurred: {}'.format(str(e))}), 500
        
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
