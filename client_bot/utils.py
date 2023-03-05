import telegram


def update_conversation_state(
    db,
    tg_user_id: str,
    new_conversation_state: str
) -> None:
    _, current_tg_user_id, current_conversation_state = db.get_client(
        tg_user_id=tg_user_id
    )[0]
    if current_conversation_state != new_conversation_state:
        db.update_client(
            tg_user_id=current_tg_user_id,
            conversation_state=new_conversation_state
        )


def safely_send_message(
    bot: telegram.Bot,
    **send_message_kwargs
) -> None:
    """Send message to specific chat by specific bot.

    Display error message if something went wrong
    """
    try:
        bot.send_message(
            **send_message_kwargs
        )
    except (telegram.error.BadRequest, telegram.error.Unauthorized) as error:
        error_msg = f"[DBG] -> expert_bot -> utils.py -> safely_send_message -> {error}"
        print(error_msg)


def send_text_to_all_experts(
    db,
    bot,
    **send_message_kwargs
) -> None:
    for expert_id, expert_tg_user_id in db.get_all_experts():
        safely_send_message(
            bot=bot,
            chat_id=expert_tg_user_id,
            **send_message_kwargs
        )
