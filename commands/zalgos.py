from zalgo_text import zalgo
import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    #log(update, lang["zalgo.log"])

    try:
        message = update.message.reply_to_message.text
        # Reply to message
        context.bot.send_message(chat_id=update.effective_chat.id, text=zalgo.zalgo().zalgofy(message),
                                 reply_to_message_id=update.message.reply_to_message.message_id)
    # Exceptions
    except AttributeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["zalgo.invalid"])
    except TypeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["zalgo.invalid"])