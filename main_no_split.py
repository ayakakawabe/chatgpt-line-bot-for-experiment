import os
import sys
from argparse import ArgumentParser
from dotenv import load_dotenv

from flask import Flask, request, abort
from linebot.v3 import (
     WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

from openai import OpenAI
import csv
import datetime

#----settings----/
load_dotenv()

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

client=OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)
#/----settings----



openai_params=[
    {"role": "system", "content": "You are user's friend. Reply a short answer."},
    {"role": "assistant","content":"はじめまして！よろしくね"}
  ]


def adjust_num_of_lines(openai_params):
    if(len(openai_params)>10):
        del openai_params[1]

def response_openai(openai_params):
    adjust_num_of_lines(openai_params)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=openai_params
    )
    response_text=completion.choices[0].message.content
    return response_text



def write_csv(user_data,bot_data):
    with open('csv/data_no_split.csv', 'a',encoding='utf_8_sig',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user",user_data])
        writer.writerow(["bot",bot_data])

def write_csv_timestamp(bot_time,user_time):
    with open('csv/timestamp_no_split.csv', 'a',encoding='utf_8_sig',newline="") as f:
        writer = csv.writer(f)
        writer.writerow([bot_time,user_time])


def write_csv_start_info():
    date=datetime.datetime.now()
    with open('csv/data_no_split.csv', 'a',encoding='utf_8_sig',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["experiment-date",date])
    with open('csv/timestamp_no_split.csv', 'a',encoding='utf_8_sig',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["experiment-date",date])
        writer.writerow(["bot","user"])

write_csv_start_info()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

bot_timestamp=0

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    global bot_timestamp
    user_timestamp=event.timestamp/1000
    print("user:",event.message.text)
    print("user:",user_timestamp)
    openai_params.append({"role": "user", "content": event.message.text})
    response_message_text=response_openai(openai_params)
    print("bot:",response_message_text)
    write_csv(event.message.text,response_message_text)
    write_csv_timestamp(bot_timestamp,user_timestamp)
    openai_params.append({"role": "assistant", "content": response_message_text})
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_message_text)]
            )
        )
    bot_timestamp=datetime.datetime.timestamp(datetime.datetime.now())
    print("bot:",bot_timestamp)
    


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host="0.0.0.0", port=5000, debug=False)