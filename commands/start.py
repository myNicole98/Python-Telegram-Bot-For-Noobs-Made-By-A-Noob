import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    #log(update, lang["start.log"])
    # Send message
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=lang["start.send_message"],
                             parse_mode='markdown')