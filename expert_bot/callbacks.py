from telegram import Update
from telegram.ext import CallbackContext

from expert_bot.decorators import only_experts
from expert_bot.texts import (end_conversation_reply, start_cmd_reply,
                              tip_use_replies_to_communicate_reply)
from expert_bot.utils import (parse_client_tg_user_id,
                              parse_notification_message, safely_send_message)


@only_experts
def start_cmd_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.effective_chat is None:
        raise ValueError("update.effective_chat is None")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_cmd_reply
    )


@only_experts
def end_message_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.message.reply_to_message:
        # Send end message to Client
        client_tg_bot = context.bot_data["client_tg_bot"].bot
        client_tg_user_id = parse_client_tg_user_id(
            client_message_text=update.message.reply_to_message.text
        )
        safely_send_message(
            bot=client_tg_bot,
            chat_id=client_tg_user_id,
            text=end_conversation_reply
        )
        # Update Client conversation state
        db = context.bot_data["my_psql_database"]
        new_conversation_state = "/start"
        db.update_client(
            tg_user_id=str(client_tg_user_id),
            conversation_state=new_conversation_state
        )
    else:
        update.message.reply_text(
            text=tip_use_replies_to_communicate_reply,
            quote=True
        )


@only_experts
def notify_message_cb(
    update: Update,
    context: CallbackContext
) -> None:
    db = context.bot_data["my_psql_database"]
    client_tg_bot = context.bot_data["client_tg_bot"].bot
    notification_text = parse_notification_message(
        expert_message_text=update.message.text
    )
    for _, client_tg_user_id, _ in db.get_all_clients():
        safely_send_message(
            bot=client_tg_bot,
            chat_id=client_tg_user_id,
            text=notification_text
        )


@only_experts
def any_message_cb(
    update: Update,
    context: CallbackContext
) -> None:
    to_skip = (
        (
            bool(update.message.reply_to_message)
            and
            update.message.text.lower() in ('end', 'кінець')
        )
        or
        (
            update.message.text.lower().startswith('розсилка')
        )
    )
    if to_skip:
        return

    if update.message.reply_to_message:
        client_tg_bot = context.bot_data["client_tg_bot"].bot
        client_tg_user_id = parse_client_tg_user_id(
            client_message_text=update.message.reply_to_message.text
        )
        safely_send_message(
            bot=client_tg_bot,
            chat_id=client_tg_user_id,
            text=update.message.text
        )
    else:
        update.message.reply_text(
            text=tip_use_replies_to_communicate_reply,
            quote=True
        )
