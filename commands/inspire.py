import requests


def init(update, context):
    #log(update, lang["inspire.log"])

    # retrieve image from source
    f = r"http://inspirobot.me/api?generate=true"
    page = requests.get(f)
    imgurl = page.text

    # Send retrieved image
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=imgurl)