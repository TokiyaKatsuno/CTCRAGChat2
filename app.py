from flask import Flask, request, jsonify, render_template
import AskChat

# Flaskアプリケーションを初期化
app = Flask(__name__)

# ルートエンドポイントの作成
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simpleChat')
def simpleChat():
    return render_template('simpleChat.html')

@app.route('/askChat')
def askChat():
    return render_template('askChat.html')

@app.route('/modifyAnswer')
def modifyAnswer():
    return render_template('modifyAnswer.html')

@app.route('/api/chat', methods=['POST'])
def addPrompt():
    user_input = request.json.get('message', '')
    AIChat_response_html = AskChat.addPrompt(user_input)
    return jsonify({'response': AIChat_response_html}), 200
    

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)