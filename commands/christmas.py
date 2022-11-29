from localization.localization import lang
from datetime import datetime

def christmas(update, context):

    date_format = "%m/%d/"

    now = datetime.now()
    xmas = datetime(now.year, 12, 25)
    delta = xmas - now
    final = delta.days
    if final > 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="\U000026C4 " +
                                        str(final) +
                                        lang["christmas.days"] + " \U0001F384",
                                    parse_mode="markdown")
    elif final == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="\U000026C4 " +
                                        lang["christmas.xmas"] + " \U0001F384",
                                    parse_mode="markdown")