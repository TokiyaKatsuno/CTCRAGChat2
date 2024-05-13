# Chatの動作確認
ベクトルDB(PGVector)から、もっとも類似度の高いデータをベクトル検索し、
ChatGPTで応答を生成するChatの動作確認を行います。
本ChatはFlaskをベースとしています。

## シンプルなチャット（SimpleChat）の動作確認
SimpleChat.pyを選択し、F5で実行してください。
![alt text](/Chat/images/シンプルチャット起動方法.png)
動作イメージ
![alt text](/Chat/images/シンプルチャット動作イメージ.png)

## 問診チャット（AskChat）の動作確認
AskChat.pyを選択し、F5で実行してください。
動作イメージ
![alt text](/Chat/images/問診チャット動作イメージ.png)

## 前提条件
環境はセキュアPC（Windows11）にWSL(Ubuntu)です。
PGVectorのインストールやデータ登録は、こちらの[README.md](../PGVector/README.md)を参照してください。

## 必要なライブラリのインストール
Flask等のライブラリをインストールします。
```
pip3 install -r requirements.txt
```
 
## PostgreSQLの起動
```
sudo service postgresql start
```
 
## flaskの起動
VSCodeでapp.pyを開き、F5で実行してください。
## 参考：
- ChatGPT Plusに「flaskでChatGPTのAPIと会話するチャットUIのプログラムを作成して」
