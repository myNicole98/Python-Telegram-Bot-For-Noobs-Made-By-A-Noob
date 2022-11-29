from localization.localization import lang
from owoify import Owoifator

owoifator = Owoifator()

def owo(update, context):
    try:
        message = update.message.reply_to_message.text
        # Reply to message
        context.bot.send_message(chat_id=update.effective_chat.id, text=owoifator.owoify(message),
                                    reply_to_message_id=update.message.reply_to_message.message_id)
    # Exceptions
    except AttributeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["owo.invalid"])
    except TypeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["owo.invalid"])