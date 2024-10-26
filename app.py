from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='mWI7mV64QqV0Xm0dUqNBnx11/OJDoUrCPW1EmdnHD9IH3T3JKt5pVQwkvHQ9c0Eox7q9AixzEQT11YIvL7AFdlUvCzrH4rbBtIBCL+e4zuciLqP+aPd/xKcHqNNBVHI6Zg7oyMFWt6aM3qxHfTPovAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8c2db28559ea38b8e80ac0f230863e8e')


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg = event.message.text
    r = "您的問題機器人無法回應，請稍後由專人為您服務^^"

    if msg.lower() == 'hi':
        r = 'hi'
    elif msg == '嗨':
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒，有推薦的嗎？'

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=r)]
            )
        )

if __name__ == "__main__":
    app.run()