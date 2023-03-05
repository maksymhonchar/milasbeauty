import queue
from typing import Dict, List

import telegram
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          Handler, MessageHandler)

from client_bot.callbacks import *


class ClientTGBot:

    def __init__(
        self,
        token: str
    ) -> None:
        self.bot = telegram.Bot(token)
        self.dispatcher = telegram.ext.Dispatcher(
            bot=self.bot,
            update_queue=queue.Queue()
        )
        self._add_handlers()

    def _add_handlers(
        self
    ) -> None:
        DEFAULT_GROUP = 0
        GLOBALS_GROUP = 1
        handlers_storage: Dict[int, List[Handler]] = {
            DEFAULT_GROUP: [
                CommandHandler(
                    command="start",
                    callback=start_cb
                ),
                MessageHandler(
                    filters=Filters.regex("^(б’юті консьерж)$"),
                    callback=beauty_concierge_cb
                ),
                MessageHandler(
                    filters=Filters.regex("^(поділитись відгуком)$"),
                    callback=feedback_cb
                ),
                MessageHandler(
                    filters=Filters.regex("^(Q & A)$"),
                    callback=q_and_a_cb
                ),
            ],
            GLOBALS_GROUP: [
                MessageHandler(
                    filters=(
                        Filters.text &
                        (~ Filters.regex("^(б’юті консьерж)$")) &
                        (~ Filters.regex("^(поділитись відгуком)$")) &
                        (~ Filters.regex("^(Q & A)$")) &
                        (~ Filters.command)
                    ),
                    callback=any_message_cb
                ),
                CallbackQueryHandler(
                    callback=any_callbackquery_cb
                ),
            ]
        }
        for group, handlers in handlers_storage.items():
            for handler in handlers:
                self.dispatcher.add_handler(
                    handler=handler,
                    group=group
                )
