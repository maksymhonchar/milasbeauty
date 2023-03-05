from typing import List, Optional

from telegram import Update
from telegram.ext import CallbackContext

from client_bot.keyboards import *
from client_bot.texts import *
from client_bot.utils import (send_text_to_all_experts,
                              update_conversation_state)


def start_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.effective_chat is None:
        raise ValueError("update.effective_chat is None")
    if update.effective_user is None:
        raise ValueError("update.effective_user is None")

    # Add new client if necessary. Otherwise update state as usual
    db = context.bot_data["my_psql_database"]
    current_tg_user_id = str(update.effective_user.id)
    conversation_state = '/start'
    current_client = db.get_client(
        tg_user_id=current_tg_user_id
    )
    if not current_client:
        db.add_client(
            tg_user_id=current_tg_user_id,
            conversation_state=conversation_state
        )
    else:
        update_conversation_state(
            db=context.bot_data["my_psql_database"],
            tg_user_id=str(update.effective_user.id),
            new_conversation_state=conversation_state
        )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_cmd_reply,
        reply_markup=main_keyboard_markup
    )


def beauty_concierge_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.effective_chat is None:
        raise ValueError("update.effective_chat is None")
    if update.effective_user is None:
        raise ValueError("update.effective_user is None")

    conversation_state = 'beauty_concierge'
    update_conversation_state(
        db=context.bot_data["my_psql_database"],
        tg_user_id=str(update.effective_user.id),
        new_conversation_state=conversation_state
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=beauty_concierge_cmd_start_reply,
        reply_markup=main_keyboard_markup
    )


def feedback_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.effective_chat is None:
        raise ValueError("update.effective_chat is None")
    if update.effective_user is None:
        raise ValueError("update.effective_user is None")

    conversation_state = 'feedback'
    update_conversation_state(
        db=context.bot_data["my_psql_database"],
        tg_user_id=str(update.effective_user.id),
        new_conversation_state=conversation_state
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=feedback_cmd_start_reply
    )


def q_and_a_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.effective_chat is None:
        raise ValueError("update.effective_chat is None")
    if update.effective_user is None:
        raise ValueError("update.effective_user is None")

    conversation_state = 'q_and_a'
    update_conversation_state(
        db=context.bot_data["my_psql_database"],
        tg_user_id=str(update.effective_user.id),
        new_conversation_state=conversation_state
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=q_and_a_cmd_reply,
        reply_markup=q_and_a_inline_keyboard_markup
    )


def any_message_cb(
    update: Update,
    context: CallbackContext
) -> None:
    if update.effective_user is None:
        raise ValueError("update.effective_user is None")
    if update.message.from_user is None:
        raise ValueError("update.message.from_user is None")
    if update.effective_chat is None:
        raise ValueError("update.effective_chat is None")

    db = context.bot_data["my_psql_database"]
    _, current_tg_user_id, current_conversation_state = db.get_client(
        tg_user_id=str(update.effective_user.id)
    )[0]

    if current_conversation_state == 'feedback':
        # Send message to all experts
        expert_tg_bot = context.bot_data["expert_tg_bot"].bot
        expert_text = feedback_message_to_expert.format(
            from_user_tg_username=(
                update.message.from_user["username"]
                or
                "Клієнт має пустий юзернейм :)"
            ),
            from_user_tg_id=update.message.from_user["id"],
            client_text=update.message.text
        )
        send_text_to_all_experts(
            db=db,
            bot=expert_tg_bot,
            text=expert_text
        )
        # Send reply message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=feedback_next_step_reply
        )
        # Update Client state
        new_conversation_state = "feedback_2"
        db.update_client(
            tg_user_id=current_tg_user_id,
            conversation_state=new_conversation_state
        )
    elif current_conversation_state == "feedback_2":
        print(
            f'[DBG] -> client_bot -> callbacks.py -> any_message_cb -> feedback_2 -> {update.message.text=}'
        )
        # Send message to all experts
        expert_tg_bot = context.bot_data["expert_tg_bot"].bot
        expert_text = feedback_message_to_expert.format(
            from_user_tg_username=(
                update.message.from_user["username"]
                or
                "Клієнт має пустий юзернейм :)"
            ),
            from_user_tg_id=update.message.from_user["id"],
            client_text=update.message.text
        )
        send_text_to_all_experts(
            db=db,
            bot=expert_tg_bot,
            text=expert_text
        )
        #
        if update.message.text.lower() in ('ні', 'ні дякую', 'ні, дякую', 'дякую ні', 'дякую, ні', 'нє'):
            # Send reply message
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=feedback_cmd_end_reply
            )
            # Update Client state
            new_conversation_state = "/start"
            db.update_client(
                tg_user_id=current_tg_user_id,
                conversation_state=new_conversation_state
            )
    elif current_conversation_state == 'beauty_concierge':
        # Send message to all experts
        expert_tg_bot = context.bot_data["expert_tg_bot"].bot
        expert_text = beauty_concierge_message_to_expert.format(
            from_user_tg_username=(
                update.message.from_user["username"]
                or
                "Клієнт має пустий юзернейм :)"
            ),
            from_user_tg_id=update.message.from_user["id"],
            client_text=update.message.text
        )
        send_text_to_all_experts(
            db=db,
            bot=expert_tg_bot,
            text=expert_text
        )


def any_callbackquery_cb(
    update: Update,
    context: CallbackContext
) -> None:
    query = update.callback_query
    query.answer()

    reply_mapping = {
        "shop_inline_button_click": q_and_a_shop_reply,
        "delivery_inline_button_click": q_and_a_delivery_reply,
        "payment_inline_button_click": q_and_a_payment_reply,
        "certificate_inline_button_click": q_and_a_certificate_reply,
    }
    reply_text = reply_mapping.get(
        query.data,
        "ERROR_MISSING_KEY_IN_REPLY_MAPPING"
    )
    query.edit_message_text(
        text=reply_text,
        parse_mode='HTML'
    )
