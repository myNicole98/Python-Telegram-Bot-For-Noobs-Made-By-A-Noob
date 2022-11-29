import json, requests

def doggo(update, context):

    # retrieve image from source
    f = r"https://random.dog/woof.json"
    page = requests.get(f)
    data = json.loads(page.text)
    # Send retrieved image
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                            photo=data["url"], caption="(❍ᴥ❍ʋ)")