import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    #log(update, lang["help.log"])

    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=lang["help.send_message"])