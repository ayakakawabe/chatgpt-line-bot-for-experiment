# chatgpt-line-bot-for-experiment

# 概要

ChatGPTが返信するLINE bot

送受信メッセージとタイムスタンプがcsvファイルに保存される

1. 13文字前後になるように分割して返信するbot
2. 分割なしで返信するbot

## csvファイルの例

* data_***.csv
  * experiment-date:実験日時
  * id:id
  * speak:送信者(user/bot)
  * content:送信内容
    
* timestamp_***.csv
  * experiment-date:実験日時
  * id:id
  * bot:botのタイムスタンプ（秒）
  * user:userのタイムスタンプ（秒）
    
### data_split.csv
```
experiment-date,2023-11-15 23:58:35.416064
id,speak,content
1,user,こんにちは
2,bot,こんにちは！元気ですか？
2,user,元気！
3,bot,それは良かったですね！
3,bot,何かおもしろいことがありましたか？
3,user,えーとね
4,bot,何か特別なことでもありましたか？

experimentdate,2023-11-16 21:58:35.000064
id,speak,content
1,user,こんにちは
2,bot,こんにちは！元気ですか？
```

### timestamp_split.csv
```
DON'T use the first data.(bot=0)

experiment-date,2023-11-15 23:58:35.416064
id,bot,user
1,0,1700060316.607
2,1700060319.046153,1700060322.043
3,1700060325.001803,1700060327.211

experiment-date,2023-11-15 23:58:35.416064
id,bot,user
1,0,1700060316.607
2,1700060319.046153,1700060322.043
```

### data_no_split.csv
```
experiment-date,2023-11-15 23:52:27.656900
id,speak,content
1,user,こんにちは
2,bot,こんにちは！元気？
2,user,元気！
3,bot,それは良かった！何かおもしろいことがあった？
3,user,えーとね
4,bot,何かしら面白いことがあったのかな？
```

### timestamp_no_split.csv
```
DON'T use the first data.(bot=0)

experiment-date,2023-11-15 23:52:27.656900
id,bot,user
1,0,1700059949.145
2,1700059951.702995,1700059953.467
3,1700059956.667543,1700059959.94
```


# 開発環境

* Windows10
* Python 3.11.3
* pip 23.1.2
* flask 3.0.0
* openai 1.2.4
* ptrhon-dotenv 1.0.0
* line-bot-sdk 3.5.0

# 設定

## ライブラリのインストール
```
pip install -r requirements.txt
```

## LINE Developersの設定

[Messaging API](https://developers.line.biz/ja/docs/messaging-api/getting-started/) でチャネルを作成し、チャネルアクセストークンとチャネルシークレットを取得する

* 応答メッセージ・あいさつメッセージを無効にする
* Webhookの利用を有効

## フォルダ構成

```
.
├── .gitignore
├── .env
├── csv
│   ├── data_no_split.csv
│   ├── data_split.csv
│   ├── timestamp_no_split.csv
│   └── timestamp_split.csv
├── main_ni_split.py
├── main_split.py
└── requirements.txt
```

### .envの作成

1. ルートディレクトリに.envを作成する

```
LINE_CHANNEL_ACCESS_TOKEN='YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET='YOUR_CHANNEL_SECRET'
OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
```

2. 'YOUR_CHANNEL_ACCESS_TOKEN'と'YOUR_CHANNEL_SECRET'を、Messaging API で取得したチャネルアクセストークンとチャネルシークレットに変更する

3. 'YOUR_OPENAI_API_KEY'をOpenAIのAPIキーに変更する


## webhookの設定

[ngrok](https://ngrok.com/) でローカル環境を外部公開する

### ngrokの設定
[ngrok](https://ngrok.com/)をダウンロード



# 実行
※分割なし/ありを同時に立ち上げないこと！

## 分割なしの場合

1. localhostを起動
```
python main_no_split.py
```

2. ngrokで外部公開
```
$ ngrok http 5000
```

3. Messaging APIのwebhookURLにngrokで取得したURL+'/callback'を入力する
  Ex.)https://XXXXXXXX.ngrok-free.app/callback

4. webhookURLの検証をクリック
→「成功」と表示されればOK

5. Messaging API のQRコードからLINEで友達追加して操作する


## 分割ありの場合

1. localhostを起動
```
python main_split.py
```

2. ngrokで外部公開
```
$ ngrok http 5000
```

3. Messaging APIのwebhookURLにngrokで取得したURL+'/callback'を入力する
  Ex.)https://XXXXXXXX.ngrok-free.app/callback

4. webhookURLの検証をクリック
→「成功」と表示されればOK

5. Messaging API のQRコードからLINEで友達追加して操作する
