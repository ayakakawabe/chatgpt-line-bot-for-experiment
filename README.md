# chatgpt-line-bot-for-experiment

## 概要

ChatGPTが返信するLINE bot
* 13文字前後になるように分割して返信するbot
* 分割なしで返信するbot


送受信メッセージとタイムスタンプがcsvファイルに保存される

![システム構成イメージ](https://github.com/ayakakawabe/chatgpt-line-bot-for-experiment/assets/103473179/200b8603-aebe-4ac4-b92a-c354416d6309)


### csvファイルの例

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
    
#### data_split.csv
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

#### timestamp_split.csv
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

#### data_no_split.csv
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

#### timestamp_no_split.csv
```
DON'T use the first data.(bot=0)

experiment-date,2023-11-15 23:52:27.656900
id,bot,user
1,0,1700059949.145
2,1700059951.702995,1700059953.467
3,1700059956.667543,1700059959.94
```


## 開発環境

* Windows10
* Python 3.11.3
* pip 23.1.2
* flask 3.0.0
* openai 1.2.4
* ptrhon-dotenv 1.0.0
* line-bot-sdk 3.5.0

## 💡使用方法

## 設定

1. このgithubから、Code > Download ZIP
2. ダウンロードしたzipファイルを展開
3. VScodeを開いて、 file > Open folder > chatgpt-line-bot-for-experiment（展開後のファイル）> chatgpt-line-bot-for-experiment > 開く

   （二つ目の「chatgpt-line-bot-for-experiment」で開く）

### ライブラリのインストール(VScodeのterminal)
```
pip install -r requirements.txt
```

### LINE Developersの設定

1. [Messaging API](https://developers.line.biz/ja/docs/messaging-api/getting-started/) でチャネルを作成する
2. MessagingAPI設定 > 長期チャネルアクセストークンを発行する
3. チャネルアクセストークンとチャネルシークレットを取得し、メモしておく

* 応答メッセージを無効にする
* Webhookの利用・あいさつメッセージを有効（[Isuees:To-do](https://github.com/ayakakawabe/chatgpt-line-bot-for-experiment/issues/1)参照）
* あいさつメッセージ：
  ```
  ○○さん
  はじめまして！最近買ったものについて教えて！
  ```
### フォルダ構成

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

#### .envの作成

1. ルートディレクトリに.envを作成する

   （VScodeで、左側上部chatgpt-line-bot-for-experimentの横の**New File...**をクリックし、**.env**と入力）

```
LINE_CHANNEL_ACCESS_TOKEN='YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET='YOUR_CHANNEL_SECRET'
OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
LINE_CHANNEL_ACCESS_TOKEN_SPLIT='YOUR_CHANNEL_ACCESS_TOKEN_SPLIT'
LINE_CHANNEL_SECRET_SPLIT='YOUR_CHANNEL_SECRET_SPLIT'
```

2. 'YOUR_CHANNEL_ACCESS_TOKEN'と'YOUR_CHANNEL_SECRET'を、Messaging API で取得したチャネルA(分割なし)チャネルアクセストークンとチャネルシークレットに変更する
3. 'YOUR_CHANNEL_ACCESS_TOKEN_SPLIT'と'YOUR_CHANNEL_SECRET_SPLIT'を、Messaging API で取得したチャネルB(分割あり)チャネルアクセストークンとチャネルシークレットに変更する

4. 'YOUR_OPENAI_API_KEY'をOpenAIのAPIキーに変更する


### webhookの設定

[ngrok](https://ngrok.com/) でローカル環境を外部公開する

#### ngrokの設定
1. [ngrok](https://ngrok.com/)をダウンロード
2. 公式サイトの手順に従って設定する
3. `ngrok`コマンドのパスを通す（Windows→[Windowsの環境パスを通す](https://realize.jounin.jp/path.html)）



## 実行
※分割なし/ありを同時に立ち上げないこと！

### 分割なしの場合

1. localhostを起動（VScodeのterminal）
```
python main_no_split.py
```

2. ngrokで外部公開（terminal）
```
$ ngrok http 5000
```
3. Terminalに表示されているURL+'/hello'をブラウザで表示させる
   Ex.)https://XXXXXXXX.ngrok-free.app/hello

   「visit site」をクリック→「**NO_SPLIT**」と表示されればOK

4. Messaging APIのwebhookURLにngrokで取得したURL+'/callback'を入力する
  Ex.)https://XXXXXXXX.ngrok-free.app/callback

5. webhookURLの検証をクリック
→「成功」と表示されればOK

6. Messaging API のQRコードからLINEで友達追加して操作する


### 分割ありの場合

1. localhostを起動（VScodeのterminal）
```
python main_split.py
```

2. ngrokで外部公開（terminal）
```
$ ngrok http 5000
```
3. Terminalに表示されているURL+'/hello'をブラウザで表示させる
   Ex.)https://XXXXXXXX.ngrok-free.app/hello

   「visit site」をクリック→「**YES_SPLIT**」と表示されればOK
   
5. Messaging APIのwebhookURLにngrokで取得したURL+'/callback'を入力する
  Ex.)https://XXXXXXXX.ngrok-free.app/callback

4. webhookURLの検証をクリック
→「成功」と表示されればOK

5. Messaging API のQRコードからLINEで友達追加して操作する

## 🧪実験時
（使用方法は一通り終わらせている前提で）
1. VScodeを開く
2. file > Open folder > chatgpt-line-bot-for-experiment（展開後のファイル）> chatgpt-line-bot-for-experiment > 開く

   （二つ目の「chatgpt-line-bot-for-experiment」で開く）
3. VScode上部のTerminal > New Terminal （1つ目のterminal）
4. VScodeのTerminalの左側の＋ボタンをクリック （2つ目のterminal）


※分割なし/ありを同時に立ち上げないこと！

### 分割なし → 分割ありの場合

1. 分割なしのlocalhostを起動（1つ目のterminal）
```
python main_no_split.py
```

2. ngrokで外部公開（2つ目のterminal）
```
$ ngrok http 5000
```
3. Terminalに表示されているURL+'/hello'をブラウザで表示させる
   Ex.)https://XXXXXXXX.ngrok-free.app/hello

   「visit site」をクリック→「**NO_SPLIT**」と表示されればOK

4. Messaging APIの**チャネルA**のwebhookURLにngrokで取得したURL+'/callback'を入力する
  Ex.)https://XXXXXXXX.ngrok-free.app/callback

5. webhookURLの検証をクリック

   →「成功」と表示されればOK

7. Messaging API のチャネルAをQRコードからLINEで友達追加して操作する
8. **分割内なしの実験が終わったら**、**1つ目**のterminalで`Ctrl+C`
9. 分割ありのlocalhostを起動（1つ目のterminal）
```
python main_split.py
```
9. 3で開いたURLをリロード

    →「**YES_SPLIT**」と表示されればOK

10. Messaging API**のチャネルB**のwebhookURLに4で入力したURLを入力
11. webhookURLの検証をクリック

    →「成功」と表示されればOK
12. Messaging API のチャネルBをQRコードからLINEで友達追加して操作する


### 分割あり → 分割なしの場合

1. 分割なしのlocalhostを起動（1つ目のterminal）
```
python main_split.py
```

2. ngrokで外部公開（2つ目のterminal）
```
$ ngrok http 5000
```
3. Terminalに表示されているURL+'/hello'をブラウザで表示させる
   Ex.)https://XXXXXXXX.ngrok-free.app/hello

   「visit site」をクリック→「**YES_SPLIT**」と表示されればOK

4. Messaging APIの**チャネルB**のwebhookURLにngrokで取得したURL+'/callback'を入力する
  Ex.)https://XXXXXXXX.ngrok-free.app/callback

5. webhookURLの検証をクリック

   →「成功」と表示されればOK

7. Messaging API のチャネルBをQRコードからLINEで友達追加して操作する
8. **分割内ありの実験が終わったら**、**1つ目**のterminalで`Ctrl+C`
9. 分割ありのlocalhostを起動（1つ目のterminal）
```
python main_no_split.py
```
9. 3で開いたURLをリロード

    →「**NO_SPLIT**」と表示されればOK

10. Messaging API**のチャネルA**のwebhookURLに4で入力したURLを入力
11. webhookURLの検証をクリック

    →「成功」と表示されればOK
12. Messaging API のチャネルAをQRコードからLINEで友達追加して操作する


## 💻分析方法
### 実験後のcsvファイルの整形

analysis/response-time/csv/format_timestamp_no_split.csv
```
user_id	id	reaction_time
1	2	16.64851999
1	3	6.560580015
1	4	16.56498981
1	5	40.60481
2	2	4.208449841
2	3	11.83561993
2	4	19.34963989
2	5	25.66398001
```

analysis/response-time/csv/format_timestamp_split.csv
```
user_id	id	reaction_time
1	2	1.782169819
1	3	17.83516002
1	4	6.924889803
1	5	10.48215008
1	6	3.929570198
2	2	3.110630035
2	3	9.140679836
```
### 質問紙調査
#### 人格的印象（Q1-Q4）/機能的印象（Q5-Q10）
1. 回答結果のExcelからデータを取り出す
   ```
   ID,Q1,Q2,Q3,Q4
   ```
2. データの置換
   1. 全くそう思わない → 1
   2. そう思わない → 2
   3. どちらともいえない → 3
   4. 非常にそう思う → 5
   5. そう思う → 4
3. IDごとに平均を算出
4. データ整形
   ```
   ID,no split,split
   ```

#### 愛嬌を感じるか（Q11）
1. 回答結果のExcelからデータを取り出す
   ```
   ID,Q11
   ```
2. データの置換
   1. そう思わない → 0
   2. そう思う → 1
3. データ整形
   ```
   ID,no split,split
   ```
#### 自由記述
1. 回答結果のExcelからデータを取り出す
2. データ整形
   ```
   テキスト,分割
   自由記述の内容,分割あり/分割なし
   ```
3. KHcoderで共起ネットワーク図を作成
