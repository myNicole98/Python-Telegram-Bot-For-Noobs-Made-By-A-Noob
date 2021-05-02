import requests
import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    #log(update, lang["doggo.log"])

    # retrieve image from source
    f = r"https://random.dog/woof.json"
    page = requests.get(f)
    data = json.loads(page.text)
    # Send retrieved image
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=data["url"], caption="(❍ᴥ❍ʋ)")