from commands import start, help, trans, owo, zalgos, doggo, pisi, inspire, spectral, meme, unsplash, tweet, christmas, pap, slap, aouguri
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, Updater
import json

# Bot language - Available languages are located in the "localization" folder
with open("localization/en_US.json", "r", encoding='utf-8') as f:
    lang = json.load(f)

# Batch size for memes. Higher values = less repetition = higher download time
batch = 100

# Load credentials
with open("credentials.json", "r") as f:
    credentials = json.load(f)
# Bot init
updater = Updater(token=credentials["token"], use_context=True)
dispatcher = updater.dispatcher

# cmd handlers
start_handler = CommandHandler('start', start.start)
help_handler = CommandHandler('help', help.help)
trans_handler = CommandHandler('trans', trans.trans)
owo_handler = CommandHandler('owo', owo.owo)
doggo_handler = CommandHandler('doggo', doggo.doggo)
pisi_handler = CommandHandler('pisi', pisi.pisi)
spectral_handler = CommandHandler('spectral', spectral.spectral)
zalgo_handler = CommandHandler('zalgo', zalgos.zalgos)
meme_handler = CommandHandler('meme', meme.meme)
unsplash_handler = CommandHandler("unsplash", unsplash.unsplash)
aouguri_handler = CommandHandler("aouguri", aouguri.aouguri)
christmas_handler = CommandHandler("christmas", christmas.christmas)
pap_handler = CommandHandler("pap", pap.pap)
slap_handler = CommandHandler("slap", slap.slap)
inspire_handler = CommandHandler("inspire", inspire.inspire)

# conversation handlers
tweet_handler = ConversationHandler(
    entry_points=[CommandHandler('tweet', tweet.tweet_start)],
    states={
        tweet.PF: [MessageHandler(Filters.all, tweet.tweet_profile_picture)],
        tweet.name: [MessageHandler(Filters.all, tweet.tweet_name)],
        tweet.username: [MessageHandler(Filters.all, tweet.tweet_username)],
        tweet.message: [MessageHandler(Filters.all, tweet.tweet_creator)],
    },
    fallbacks=[CommandHandler('quit', tweet.tweet_exit)],
    per_user=True
)

# cmd dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(trans_handler)
dispatcher.add_handler(owo_handler)
dispatcher.add_handler(doggo_handler)
dispatcher.add_handler(pisi_handler)
dispatcher.add_handler(spectral_handler)
dispatcher.add_handler(zalgo_handler)
dispatcher.add_handler(meme_handler)
dispatcher.add_handler(unsplash_handler)
dispatcher.add_handler(aouguri_handler)
dispatcher.add_handler(tweet_handler)
dispatcher.add_handler(christmas_handler)
dispatcher.add_handler(pap_handler)
dispatcher.add_handler(slap_handler)
dispatcher.add_handler(inspire_handler)

updater.start_polling()
