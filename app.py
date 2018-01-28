# -*- coding: utf-8 -*-
import sys
sys.path.append('./vendor')
import os
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

# Flaskアプリケーションをインスタンス化
app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

# ルーティングの設定
@app.route("/", methods=['POST'])
def callback():
    # リクエストヘッダから署名を取得
    signature = request.headers['X-Line-Signature']
    # リクエストボディを出力
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # リクエストを処理
    try:
        handler.handle(body, signature)
    # 署名が不正な場合はレスポンスコード400を返却
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# TextMessageを処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "検索":
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="最初にアーティスト名を入れて下さい")])
        artist = event.message.text
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="次に曲名を入れて下さい")])
    else:
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="「検索」と入れてみて下さい")])



# 起動
if __name__ == "_main_":
    # ログを出力
    app.debug = True;
    app.run()