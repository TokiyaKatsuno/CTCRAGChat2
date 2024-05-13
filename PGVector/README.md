# PGVectorのインストールと動作確認
PGVectorのインスールと動作確認をしてみました。
環境はセキュアPC（Windows11）にWSL(Ubuntu)です。
 
## PostgreSQLのインストール
```
sudo apt update
sudo apt upgrade
sudo apt install postgresql postgresql-contrib
```
 
## PostgreSQLの起動
```
sudo service postgresql start
```
 
## PostgreSQLの動作確認
```
sudo -u postgres psql
```
 
## PGVectorのインストール
```
cd /tmp
git clone --branch v0.6.2 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install
```
 
## PGVectorの動作確認
```
sudo -u postgres psql
```

## パスワードの変更
```
ALTER USER postgres WITH PASSWORD 'postgres';
```

### EXTENSIONの有効化
```
postgres=# CREATE EXTENSION vector;
```

### knowledgeテーブルの作成
```
postgres=# CREATE TABLE knowledge (
  knowledge_id BIGSERIAL PRIMARY KEY, 
  knowledge_text VARCHAR(100000),
  knowledge_vector VECTOR(1536), 
  knowledge_source VARCHAR(1000)
  );
```


### qaテーブルの作成
```
postgres=# CREATE TABLE qa (
  qa_id BIGSERIAL PRIMARY KEY, 
  qa_prompt VARCHAR(100000),
  qa_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  qa_answer VARCHAR(100000),
  qa_modified_answer VARCHAR(100000),
  qa_bleu DOUBLE PRECISION
  );
```
 
## VSCodeからPostgreSQLへ接続

### プラグインのインストール
VSCodeの【Extensions】から"postgresql"と検索し、一番上に出てくるPostgreSQL Management Tool をインストールする。
<img width="626" alt="image" src="https://github.com/hitomi-iizuka/work/assets/150317376/2ea73b17-f8de-409d-9fa0-aa16e38ba7a6">

### データベースとの接続
左側のサイドバーの象のアイコンがPostgreSQLプラグインである。
<img width="583" alt="image" src="https://github.com/hitomi-iizuka/work/assets/150317376/f25e2b49-a615-4b16-a0bb-d523401a5776">


こちらをクリックし、右側に現れるPOSTGRESQL EXPLORE POSTGRESQLの横の「＋」をクリックする。
<img width="584" alt="image" src="https://github.com/hitomi-iizuka/work/assets/150317376/a1b9415b-9cf6-4c34-b9c1-bcc5ba7ca820">


画面上部に接続するデータベースの接続情報を入力するバーが表示される。
<img width="637" alt="image" src="https://github.com/hitomi-iizuka/work/assets/150317376/5579efeb-6889-4fb0-830c-cf27a95e8587">

上記のバー内で「hostname」、「user」、「password」、「port number」、接続方法と順に聞かれるので以下のように入力する。
hostname:
```
127.0.0.1 
```
user:
```
postgres
```
password:
```
postgres
```
port number:
```
5432
```
接続方法:
```
Standard Connection
```
接続先databaseインスタンスの選択する。誤操作などをなるべく防ぐためpostgresのみを選択する。
<img width="641" alt="image" src="https://github.com/hitomi-iizuka/work/assets/150317376/15dacb4b-0a3f-44e8-9a2e-1bdd4f498361">


### SQLの発行
DBインスタンス名（postgres）のところにカーソルを合わせ右クリック → 「New Query」を選ぶ。ここでSQLを記述し、実行することができる。

<img width="639" alt="image" src="https://github.com/hitomi-iizuka/work/assets/150317376/aff41911-b406-4d6d-8047-6bb8d42cae34">



## PGVectorへのデータ登録と検索
### psycopg2ライブラリを使用します。
```
pip install psycopg2-binary
```

## PGVectorへのデータ登録
演習1_PGVectorへのデータ登録.pyを実行します。


## PGVectorのベクトル検索
演習2_PGVectorのベクトル検索.pyを実行します。

## 参考：
- ChatGPT Plusに「WSL（Ubuntu）にPostgreSQLのインストール手順を教えてください。」
- [GitHub - pgvector/pgvector: Open-source vector similarity search for Postgres](https://github.com/pgvector/pgvector
)
- [pgvector インデックスによる類似検索の高速化](
https://cloud.google.com/blog/ja/products/databases/faster-similarity-search-performance-with-pgvector-indexes)
