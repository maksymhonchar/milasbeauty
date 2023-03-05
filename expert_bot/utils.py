import telegram


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


def parse_notification_message(
    expert_message_text: str
) -> str:
    """Extract notification text from message"""
    return expert_message_text[len('розсилка'):].strip()


def parse_client_tg_user_id(
    client_message_text: str
) -> int:
    """Extract telegram user ID from message"""
    tokens = client_message_text.split('\n', maxsplit=2)
    return int(tokens[1])
