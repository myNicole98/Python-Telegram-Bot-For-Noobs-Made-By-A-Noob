from localization.localization import lang
def start(update, context):
    # Send message
    context.bot.send_message(chat_id=update.effective_chat.id,
                                text=lang["start.send_message"],
                                parse_mode='markdown')