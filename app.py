import datetime
import logging
import os
import sys

from flask import Flask, request
from telegram import Update

from client_bot import ClientTGBot
from database import MyPSQLDatabase
from expert_bot import ExpertTGBot

db = MyPSQLDatabase(
    dsn=os.environ.get(
        "DATABASE_URL",
        "MISSING_DATABASE_URL"
    )
)
client_tg_bot = ClientTGBot(
    token=os.environ.get(
        "CLIENT_TG_BOT_TOKEN",
        "EMPTY_TG_BOT_TOKEN"
    )
)
expert_tg_bot = ExpertTGBot(
    token=os.environ.get(
        "EXPERT_TG_BOT_TOKEN",
        "EMPTY_TG_BOT_TOKEN"
    )
)

client_tg_bot.dispatcher.bot_data["my_psql_database"] = db
expert_tg_bot.dispatcher.bot_data["my_psql_database"] = db

client_tg_bot.dispatcher.bot_data["expert_tg_bot"] = expert_tg_bot
expert_tg_bot.dispatcher.bot_data["client_tg_bot"] = client_tg_bot

flask_app = Flask(__name__)


@flask_app.route("/webhooks/client", methods=["GET", "POST"])
def webhooks_client():
    global client_tg_bot

    if request.method == "POST":
        update = Update.de_json(
            request.get_json(force=True),
            bot=client_tg_bot.bot
        )
        print(f"webhooks_client -> request.method=POST -> update is", update)
        client_tg_bot.dispatcher.process_update(update)
        return "ok"
    else:
        return "ok"


@flask_app.route("/webhooks/expert", methods=["GET", "POST"])
def webhooks_expert():
    global expert_tg_bot
    
    if request.method == "POST":
        update = Update.de_json(
            request.get_json(force=True),
            bot=expert_tg_bot.bot
        )
        print(f"webhooks_expert -> request.method=POST -> update is", update)
        expert_tg_bot.dispatcher.process_update(update)
        return "ok"
    else:
        return "ok"


if __name__ == "__main__":
    flask_app.logger.addHandler(
        logging.StreamHandler(sys.stdout)
    )
    flask_app.logger.setLevel(
        logging.DEBUG
    )

    port = int(os.environ.get('PORT', 5000))
    flask_app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
