from flask import Flask, render_template

# Flaskアプリケーションを初期化
app = Flask(__name__)

# ルートエンドポイントの作成
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/SimpleChat')
def simpleChat():
    return render_template('SimpleChat.html')

@app.route('/AskChat')
def askChat():
    return render_template('AskChat.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)