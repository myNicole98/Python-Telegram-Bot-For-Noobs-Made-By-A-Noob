import random
import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    #log(update, lang["aouguri.log"])

    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open("media/aouguri/a (" + str(random.randint(1, 5)) + ").jpg", "rb"))