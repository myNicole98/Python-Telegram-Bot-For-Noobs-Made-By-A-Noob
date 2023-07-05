import json, requests, uuid

def pisi(update, context):

    # generate unique image URL to circumvent telegram's cache
    imgurl = "https://cataas.com/cat?uid=" + str(uuid.uuid4())
    
    # send the image
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                            photo=imgurl, caption="(=^･ω･^=)")
