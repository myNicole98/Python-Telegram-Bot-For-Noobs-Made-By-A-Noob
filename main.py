from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, Updater
from PIL import Image, ImageFont, ImageDraw, ImageOps
from telegram.error import BadRequest
import warnings
import json

import commands, conversation, errors

# Variables
PF, name, username, message, done, tquit = range(6)

def main():
    #print(colored(lang["bot.is_starting"], "red"))

    # Load credentials
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    
    # Bot init
    updater = Updater(token=credentials["token"], use_context=True)
    dp = updater.dispatcher
    function = dp.add_handler


    # cmd handlers
    # ===========================================================
    function(CommandHandler('start', commands.start.init))
    function(CommandHandler('help', commands.help.init))
    function(CommandHandler('trans', commands.trans.init))
    function(CommandHandler('owo', commands.owo.init))
    function(CommandHandler('doggo', commands.doggo.init))
    function(CommandHandler('spectral', commands.spectral.init))
    function(CommandHandler('zalgo', commands.zalgos.init))
    function(CommandHandler('meme', commands.meme.init))
    function(CommandHandler("unsplash", commands.unsplash.init))
    function(CommandHandler("aouguri", commands.aouguri.init))
    function(CommandHandler("christmas", commands.christmas.init))
    function(CommandHandler("pap", commands.pap.init))
    function(CommandHandler("slap", commands.slap.init))
    function(CommandHandler("inspire", commands.inspire.init))

    # Audio menu
    function(CommandHandler("audio", commands.audio.init))
    function(CallbackQueryHandler(commands.audio.audio_submenu))
    # ===========================================================



    # Conversation Handler
    # ===========================================================
    tweet_handler = ConversationHandler(
        entry_points=[CommandHandler('tweet', conversation.tweet.tweet_start)],
        states={
            PF: [MessageHandler(Filters.all, conversation.tweet.tweet_profile_picture)],
            name: [MessageHandler(Filters.all, conversation.tweet.tweet_name)],
            username: [MessageHandler(Filters.all, conversation.tweet.tweet_username)],
            message: [MessageHandler(Filters.all, conversation.tweet.tweet_creator)],
        },
        fallbacks=[CommandHandler('quit', conversation.tweet.tweet_exit)],
        per_user=True)
    
    function(tweet_handler)
    # ===========================================================


    # Display errors and warnings
    # ===========================================================
    dp.add_error_handler(errors.log.init)              #console log
    dp.add_error_handler(errors.callback_error.init)   #channel log
    # ===========================================================

    # Ignore warnings
    warnings.filterwarnings("ignore")

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # Looooop
    main()

