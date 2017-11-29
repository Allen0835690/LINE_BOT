Usage:

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ws7um1xGlIztX9UUvKpxvI8l+kOeAYS51hitQFrC8oHM2Bb/lOdBZZf+p0stz+dmyqQ5ZJSaSLb1X/cEh8IKxBa0iH9/TKgdXI1la3SdFjLtGu4FxpY+gPuRoxlj1e1I7cxZon5aNFjXkNi1Vfs9lwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e3d42d4cee1ed348516fa10448ec76c8')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()