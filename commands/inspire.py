import requests

def inspire(update, context):

    # retrieve image from source
    f = r"http://inspirobot.me/api?generate=true"
    page = requests.get(f)
    imgurl = page.text

    # Send retrieved image
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=imgurl)