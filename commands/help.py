from localization.localization import lang
def help(update, context):

    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=lang["help.send_message"])