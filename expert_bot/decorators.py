from typing import Callable

import telegram

from expert_bot.texts import you_are_not_an_admin_reply


def only_experts(
    callback: Callable
) -> Callable:
    def wrapper(
        update: telegram.Update,
        context: telegram.ext.CallbackContext
    ) -> None:
        if update.effective_user is None:
            raise ValueError("update.effective_user is None")

        db = context.bot_data["my_psql_database"]
        current_user_tg_user_id = str(update.effective_user.id)
        expert = db.get_expert(
            tg_user_id=current_user_tg_user_id
        )
        user_is_expert = bool(expert)
        if user_is_expert:
            callback(update, context)
        else:
            update.message.reply_text(
                text=you_are_not_an_admin_reply,
                quote=True
            )

    return wrapper
