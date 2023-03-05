import re
import queue
from typing import Dict, List

import telegram
from telegram.ext import CommandHandler, Filters, Handler, MessageHandler

from expert_bot.callbacks import *


class ExpertTGBot:

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
                    callback=start_cmd_cb
                ),
                MessageHandler(
                    filters=(
                        Filters.regex(
                            pattern=re.compile(r'^(end)$', re.IGNORECASE)
                        )
                        |
                        Filters.regex(
                            pattern=re.compile(r'^(кінець)$', re.IGNORECASE)
                        )
                    ),
                    callback=end_message_cb
                ),
                MessageHandler(
                    filters=(
                        Filters.regex(
                            pattern=re.compile(r'^розсилка*', re.IGNORECASE)
                        )
                    ),
                    callback=notify_message_cb
                )
            ],
            GLOBALS_GROUP: [
                MessageHandler(
                    filters=Filters.text & ~Filters.command,
                    callback=any_message_cb
                ),
            ]
        }
        for group, handlers in handlers_storage.items():
            for handler in handlers:
                self.dispatcher.add_handler(
                    handler=handler,
                    group=group
                )
