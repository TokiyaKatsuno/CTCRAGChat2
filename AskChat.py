from flask import Flask, request, jsonify
import Common

# Flaskアプリケーションを初期化
app = Flask(__name__)

# ステップのグローバル変数
step = 0

# プロンプトのグローバル変数
user_prompt = ""

def addPrompt(user_input):
    global step
    global user_prompt
    
    AIChat_response = ""
    if (step == 0):
        user_prompt += "##事象\n"
        user_prompt += user_input + "\n"
        AIChat_response = "次に背景を教えてください。(以下の観点を参考に)　現在の状況 ／ 確認・検討のきっかけ ／ 相手方の主張・理由 ／ 達成したいこと"
        step = 1
    elif (step == 1):
        user_prompt += "##背景\n"
        user_prompt += user_input + "\n"
        AIChat_response = "関連する法令もしくは問題点・懸念点となりそうな規制や事項があれば教えてください。 "
        step = 2
    elif (step == 2):
        user_prompt += "##懸念点\n"
        user_prompt += user_input + "\n"
        
        print(f"user_prompt: {user_prompt}")
        
        # ユーザのプロンプトをベクトル化
        vector_str = Common.text2vector(user_prompt)
        
        # ベクトル検索の結果を取得
        id, similarity, knowledge_text = Common.search_similar_vector(vector_str)
        print(f"id: {id}, similarity: {similarity}, text: {knowledge_text}")

        # プロンプトの作成
        # 上記で読み込んだベクトル検索の結果を基に、詳細な指示を作成
        LLM_prompt = f"""
        #命令
        以下の「事象」が下請法として問題があるかを、「ベクトル検索の結果」に照らして有か無かで答えてください。
        {user_prompt}
        #ベクトル検索の結果
        {knowledge_text}
        # 出力形式
        下請法抵触の可能性：（有or無）
        根拠：
        対処法：
        """
        
        print(f"(LLM_prompt: {LLM_prompt}")
        
        # LLMによる回答の生成
        AIChat_response = Common.LLM_chat(LLM_prompt)
        
        # データベースにプロンプトと回答の登録
        Common.insert_data(LLM_prompt, AIChat_response)
                
        # ステップのリセット
        step = 0
        # プロンプトのリセット
        user_prompt = ""      
        
    # 改行をHTMLタグに変換
    AIChat_response_html = AIChat_response.replace("\n", r"<br \>")

    return  AIChat_response_html
    
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
