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

line_bot_api = LineBotApi('vbr2511c5fg6vzWmlKrOf5AVyZb8INO1BeDBFswAH4yCUNMKEskaBOJUaCloSFLY99fB+k1/0IqSKrwQqVUTWm0EhxSX+fUvf5eBUOrSZOgJhDVjeQGeeBBihR9yfYb7v6o1DkzsZu41RHOe7Jb8FwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6e2e681a392d3965fa717fb0214244de')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()