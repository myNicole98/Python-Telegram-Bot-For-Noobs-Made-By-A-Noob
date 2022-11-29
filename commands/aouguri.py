import random

def aouguri(update, context):

    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                            photo=open("media/aouguri/a (" + str(random.randint(1, 5)) + ").jpg", "rb"))