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
    {"role": "system", "content": "You are user's friend. Reply a short answer."}
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


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    print("user:",event.message.text)
    openai_params.append({"role": "user", "content": event.message.text})
    response_message_text=response_openai(openai_params)
    print("bot:",response_message_text)
    openai_params.append({"role": "assistant", "content": response_message_text})
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_message_text)]
            )
        )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host="0.0.0.0", port=5000, debug=True)