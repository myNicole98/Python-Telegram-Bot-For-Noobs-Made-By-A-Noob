from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, Updater
from telegram import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageFont, ImageDraw, ImageOps
from telegram.error import BadRequest
from pip._vendor import requests
from pydub import AudioSegment
from termcolor import colored
from datetime import datetime
from zalgo_text import zalgo
from urllib import request
from textwrap import wrap
from owoify import owoify
from uuid import uuid4
import warnings
import requests
import urllib
import random
import pylab
import json
import wave
import praw
import time
import os
import gc

# Bot language - Available languages are located in the "localization" folder
with open("localization/en_US.json", "r", encoding='utf-8') as f:
    lang = json.load(f)

print(colored(lang["bot.is_starting"], "red"))
# Ignore warnings
warnings.filterwarnings("ignore")

# Batch size for memes. Higher values = less repetition = higher download time
batch = 100

# Load credentials
with open("credentials.json", "r") as f:
    credentials = json.load(f)
# Bot init
updater = Updater(token=credentials["token"], use_context=True)
dispatcher = updater.dispatcher

# Variables
PF, name, username, message, done, tquit = range(6)


# Log
def log(update, log):
    try:
        t = time.localtime()
        print((colored(str(time.strftime("%d/%m/%Y %H:%M:%S", t)), "blue") + " - " +
               update.message.from_user.username + " (" + update.message.from_user.name + log))
    except TypeError:
        print((colored(str(time.strftime("%d/%m/%Y %H:%M:%S", t)), "blue") + " - " + lang["log.nousername"] + " (" +
               update.message.from_user.name + log))


# Commands
def start(update, context):
    log(update, lang["start.log"])

    # Send message
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=lang["start.send_message"],
                             parse_mode='markdown')


def help(update, context):
    log(update, lang["help.log"])

    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=lang["help.send_message"])


def trans(update, context):
    log(update, lang["trans.log"])

    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="https://bit.ly/34D6YDC")


def owo(update, context):
    log(update, lang["owo.log"])

    try:
        message = update.message.reply_to_message.text
        # Reply to message
        context.bot.send_message(chat_id=update.effective_chat.id, text=owoify(message, "uwu"),
                                 reply_to_message_id=update.message.reply_to_message.message_id)
    # Exceptions
    except AttributeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["owo.invalid"])
    except TypeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["owo.invalid"])


def zalgos(update, context):
    log(update, lang["zalgo.log"])

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


def doggo(update, context):
    log(update, lang["doggo.log"])

    # retrieve image from source
    f = r"https://random.dog/woof.json"
    page = requests.get(f)
    data = json.loads(page.text)
    # Send retrieved image
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=data["url"], caption="(❍ᴥ❍ʋ)")


def inspire(update, context):
    log(update, lang["inspire.log"])

    # retrieve image from source
    f = r"http://inspirobot.me/api?generate=true"
    page = requests.get(f)
    imgurl = page.text

    # Send retrieved image
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=imgurl)


def spectral(update, context):
    log(update, lang["spectral.log"])

    try:
        # Get file
        message = update.message.reply_to_message.audio.get_file()
        # Send message
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["spectral.analysis"])
        # Check if folders exist
        if not os.path.exists('media/audio/'):
            os.makedirs('media/audio/')
        if not os.path.exists('media/spectrogram'):
            os.makedirs('media/spectrogram')
        # Download file
        message.download("media/audio/audio.file")

        # Convert audio to mono wav
        sound = AudioSegment.from_file("media/audio/audio.file")
        sound = sound.set_channels(1)
        sound.export("media/audio/audio.wav", format="wav")

        # Create spectrogram with SoX
        os.system("sox media/audio/audio.wav -n "
                  "spectrogram -x 1024 -o media/spectrogram/spectrogram.png")

        # Create other graphs with SciPy
        def logmagnitude_spectrogram(wav_file):
            sound_info, frame_rate = get_wav_info(wav_file)
            pylab.figure(num=None, figsize=(10, 5), dpi=300)
            pylab.xscale("log")
            pylab.xlim(20, 22050)
            pylab.grid(True, which="both")
            pylab.subplot(111)
            pylab.title('Log. Magnitude Spectrum')
            pylab.magnitude_spectrum(
                sound_info, Fs=frame_rate, scale="dB", color="C1")
            pylab.savefig('media/spectrogram/spectrogram2.png', dpi=300)
            pylab.clf()
            pylab.close()
            gc.collect()

        def magnitude_spectrogram(wav_file):
            sound_info, frame_rate = get_wav_info(wav_file)
            pylab.figure(num=None, figsize=(10, 5), dpi=300)
            pylab.xlim(20, 22050)
            pylab.grid(True, which="both")
            pylab.subplot(111)
            pylab.title('Magnitude Spectrum')
            pylab.magnitude_spectrum(sound_info, Fs=frame_rate, color="C2")
            pylab.savefig('media/spectrogram/spectrogram3.png', dpi=300)
            pylab.clf()
            pylab.close()
            gc.collect()

        def phase_spectrogram(wav_file):
            sound_info, frame_rate = get_wav_info(wav_file)
            pylab.figure(num=None, figsize=(10, 5), dpi=300)
            pylab.xlim(20, 22050)
            pylab.grid(True, which="both")
            pylab.subplot(111)
            pylab.title('Phase Spectrum')
            pylab.phase_spectrum(sound_info, Fs=frame_rate, color="C3")
            pylab.savefig('media/spectrogram/spectrogram4.png', dpi=300)
            pylab.clf()
            pylab.close()
            gc.collect()

        def get_wav_info(wav_file):
            wav = wave.open(wav_file, 'r')
            frames = wav.readframes(-1)
            sound_info = pylab.fromstring(frames, 'int16')
            frame_rate = wav.getframerate()
            wav.close()
            return sound_info, frame_rate

        magnitude_spectrogram('media/audio/audio.wav')
        logmagnitude_spectrogram("media/audio/audio.wav")
        phase_spectrogram("media/audio/audio.wav")

        # Send album
        context.bot.send_media_group(chat_id=update.effective_chat.id,
                                     reply_to_message_id=update.message.reply_to_message.message_id,
                                     media=[InputMediaPhoto(media=open("media/spectrogram/spectrogram.png", "rb")),
                                            InputMediaPhoto(media=open(
                                                "media/spectrogram/spectrogram2.png", "rb")),
                                            InputMediaPhoto(media=open(
                                                "media/spectrogram/spectrogram3.png", "rb")),
                                            InputMediaPhoto(media=open("media/spectrogram/spectrogram4.png", "rb"))])
        gc.collect()
    # File size exception
    except BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=lang["spectral.file_size"],
                                 reply_to_message_id=update.message.reply_to_message.message_id)
    # Exception file extension
    except AttributeError:
        # Check if audio is a vocal message and make spectrogram
        try:
            message = update.message.reply_to_message.voice.get_file()
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=lang["spectral.analysis"])
            message.download("media/audio/vocal.file")
            sound = AudioSegment.from_file("media/audio/vocal.file")
            sound = sound.set_channels(1)
            sound.export("media/audio/vocal.wav", format="wav")

            os.system("sox media/audio/vocal.wav -n rate 16k "
                      "spectrogram -x 1024 -o media/spectrogram/spectrogram_vocal.png")

            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  reply_to_message_id=update.message.reply_to_message.message_id,
                                  photo=open('media/spectrogram/spectrogram_vocal.png', 'rb'))
        # Exception
        except AttributeError:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=lang["spectral.invalid"])


def meme(update, context):
    log(update, lang["meme.log"])

    # Reddit credentials
    reddit = praw.Reddit(client_id=credentials["reddit.client_id"],
                         client_secret=credentials["reddit.client_secret"],
                         user_agent=credentials["reddit.user_agent"])

    # Get subreddit
    subreddit = reddit.subreddit("egg_irl+traaaaaaannnnnnnnnns")

    meme = random.randint(1, 100)
    for submission in subreddit.hot(limit=meme):
        url = str(submission.url)
        caption = str(submission.title)

    # Send random meme
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=submission.url, caption=caption)


def audio_log(update, context):
    log(update, lang["audio.log"])


def unsplash(update, context):
    log(update, lang["unsplash.log"])

    # Get Y and heights
    def get_y_and_heights(text_wrapped, dimensions, margin, font):
        ascent, descent = font.getmetrics()
        line_heights = [
            font.getmask(text_line).getbbox()[3] + descent + margin
            for text_line in text_wrapped
        ]
        line_heights[-1] -= margin
        height_text = sum(line_heights)
        y = (dimensions[1] - height_text) // 2

        return y, line_heights

    '''Font type and other variables. font_type works natively on Windows. 
    I recommend using NotoColorEmoji if you're on Linux '''

    font_type = "seguiemj.ttf"
    W, H = 1920, 1080
    fontsize = 1
    V = 80
    L = 100

    # Get message
    try:
        msg = update.message.reply_to_message.text
    except AttributeError:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["unsplash.invalid"])
        return None

    text = str(msg).upper()
    if text == "NONE":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["unsplash.invalid"])
        return None

    # Write text only if shorter than 150 characters
    if len(text) <= 150:
        # Load image and fonts
        font = ImageFont.truetype(font_type, fontsize)
        if not os.path.exists('media/unsplash'):
            os.makedirs('media/unsplash/')
        urllib.request.urlretrieve(
            "https://picsum.photos/1920/1080?random=1", 'media/unsplash/unsplash_raw.jpg')
        img = Image.open("media/unsplash/unsplash_raw.jpg")
        draw_interface = ImageDraw.Draw(img)

        # Wrap text
        text_lines = wrap(text, L)
        y, line_heights = get_y_and_heights(
            text_lines,
            (W, H),
            V,
            font
        )

        # Text auto resize
        img_fraction = 0.90
        while font.getsize(text)[0] < img_fraction * img.size[0]:
            fontsize += 1
            font = ImageFont.truetype(font_type, fontsize, encoding="utf-8")
            if fontsize > 120:
                break

        # Write text
        for i, line in enumerate(text_lines):
            line_width = font.getmask(line).getbbox()[2]
            x = ((W - line_width) // 2)

            draw_interface.text((x, y), line, font=font, fill="white", stroke_width=4, stroke_fill="black",
                                anchor="lm", embedded_color=True)

            y += line_heights[i]

            # Load font for username
            fontquote = ImageFont.truetype(font_type, 35, encoding="utf-8")

            # Try first to write original sender if it's forwarded message
            try:
                username = str(
                    update.message.reply_to_message.forward_from.full_name)
                username.encode()
                draw_interface.text((1500, 720),
                                    "- " + username,
                                    font=fontquote,
                                    fill="white", stroke_width=3, stroke_fill="black", )
            except AttributeError:
                draw_interface.text((1500, 720), "- " + str(update.message.reply_to_message.from_user.full_name),
                                    font=fontquote,
                                    fill="white", stroke_width=3, stroke_fill="black", )

        # Save image and send it
        img.save('media/unsplash/unsplash.png')
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open("media/unsplash/unsplash.png", "rb"),
                              reply_to_message_id=update.message.reply_to_message.message_id)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["unsplash.too_long"])


def tweet_start(update, context):
    log(update, lang["tweet.log"])

    update.message.reply_text(lang["tweet.step1"])
    return PF


def christmas(update, context):
    log(update, lang["christmas.log"])

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


def pap(update, context):
    log(update, lang["pap.log"])

    try:
        msg = update.message.reply_to_message

        # Write user id on database
        pap_dtb = open("media/pap/pap.txt", "a")
        user_id = update.message.reply_to_message.from_user.id
        user = update.message.reply_to_message.from_user.username
        pap_dtb.write(str(user_id) + " ")
        pap_dtb.close()

        # Read recurrences of user id
        pap_file = open("media/pap/pap.txt", "r")
        pap_read = pap_file.read()
        paps = pap_read.count(str(user_id))

        # Send final message
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open("media/pap/pap.jpg", "rb"),
                              caption="Paps for @" + user + ": " + str(paps),
                              reply_to_message_id=update.message.reply_to_message.message_id)
    except AttributeError:
        return None


def slap(update, context):
    log(update, lang["slap.log"])

    try:
        msg = update.message.reply_to_message

        # Write user id on database
        slap_dtb = open("media/slap/slap.txt", "a")
        user_id = update.message.reply_to_message.from_user.id
        user = update.message.reply_to_message.from_user.username
        slap_dtb.write(str(user_id) + " ")
        slap_dtb.close()

        # Read recurrences of user id
        slap_file = open("media/slap/slap.txt", "r")
        slap_read = slap_file.read()
        slaps = slap_read.count(str(user_id))

        # Send final message
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open("media/slap/slap.jpg", "rb"),
                              caption="Slaps for @" + user + ": " + str(slaps),
                              reply_to_message_id=update.message.reply_to_message.message_id)
    except AttributeError:
        return None


def aouguri(update, context):
    log(update, lang["aouguri.log"])

    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open("media/aouguri/a (" + str(random.randint(1, 5)) + ").jpg", "rb"))


# Auxiliary functions
def audio(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    # Create keyboard
    keyboard = [
        [
            InlineKeyboardButton(lang["audio.1"], callback_data='1'),
            InlineKeyboardButton(lang["audio.2"], callback_data='2'),
        ], [
            InlineKeyboardButton(lang["audio.3"], callback_data='3'),
            InlineKeyboardButton(lang["audio.4"], callback_data='4'),
        ], [
            InlineKeyboardButton(lang["audio.5"], callback_data='5'),
            InlineKeyboardButton(lang["audio.6"], callback_data='6'),
        ], [
            InlineKeyboardButton(lang["audio.7"], callback_data='7'),
            InlineKeyboardButton(lang["audio.8"], callback_data='8'),
        ], [
            InlineKeyboardButton(lang["audio.9"], callback_data='9'),
        ], [
            InlineKeyboardButton(lang["audio.1.1"], callback_data='1.1')
        ]]

    # Send keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        update.message.reply_text(
            lang["audio.audio_guide"], reply_markup=reply_markup)
    except AttributeError:
        query.edit_message_text(lang["audio.audio_guide"])
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))


def audio_submenu(update, context):
    # Init query
    query = update.callback_query
    query.answer()

    # Answers - Sources
    if str(query.data) == str("1"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.10"], callback_data='10')],
            [InlineKeyboardButton(lang["audio.11"], callback_data='11')],
            [InlineKeyboardButton(lang["audio.12"], callback_data='12')],
            [InlineKeyboardButton(lang["audio.13"], callback_data='13')],
            [InlineKeyboardButton(lang["audio.14"], callback_data='14')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Record Player
    elif str(query.data) == str("10"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.15"], callback_data='15')],
            [InlineKeyboardButton(lang["audio.16"], callback_data='16')],
            [InlineKeyboardButton(lang["audio.17"], callback_data='17')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Audio Players
    elif str(query.data) == str("11"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.18"], callback_data='18')],
            [InlineKeyboardButton(lang["audio.19"], callback_data='19')],
            [InlineKeyboardButton(lang["audio.20"], callback_data='20')],
            [InlineKeyboardButton(lang["audio.21"], callback_data='21')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Conversion Units
    elif str(query.data) == str("2"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.22"], callback_data='22')],
            [InlineKeyboardButton(lang["audio.23"], callback_data='23')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Audio Interfaces
    elif str(query.data) == str("3"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.24"], callback_data='24')],
            [InlineKeyboardButton(lang["audio.25"], callback_data='25')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Amplifiers
    elif str(query.data) == str("4"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.26"], callback_data='26')],
            [InlineKeyboardButton(lang["audio.27"], callback_data='27')],
            [InlineKeyboardButton(lang["audio.36"], callback_data='36')],
            [InlineKeyboardButton(lang["audio.28"], callback_data='28')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Integrated
    elif str(query.data) == str("26"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.29"], callback_data='29')],
            [InlineKeyboardButton(lang["audio.30"], callback_data='30')],
            [InlineKeyboardButton(lang["audio.31"], callback_data='31')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Analogue (A & AB Class)
    elif str(query.data) == str("30"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.32"], callback_data='32')],
            [InlineKeyboardButton(lang["audio.33"], callback_data='33')],
            [InlineKeyboardButton(lang["audio.34"], callback_data='34')],
            [InlineKeyboardButton(lang["audio.35"], callback_data='35')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Preamps
    elif str(query.data) == str("36"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.37"], callback_data='37')],
            [InlineKeyboardButton(lang["audio.38"], callback_data='38')],
            [InlineKeyboardButton(lang["audio.39"], callback_data='39')],
            [InlineKeyboardButton(lang["audio.40"], callback_data='40')],
            [InlineKeyboardButton(lang["audio.41"], callback_data='41')],
            [InlineKeyboardButton(lang["audio.42"], callback_data='42')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Audio Processing
    elif str(query.data) == str("5"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.43"], callback_data='43')],
            [InlineKeyboardButton(lang["audio.44"], callback_data='44')],
            [InlineKeyboardButton(lang["audio.45"], callback_data='45')],
            [InlineKeyboardButton(lang["audio.46"], callback_data='46')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Equalizers
    elif str(query.data) == str("45"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.47"], callback_data='47')],
            [InlineKeyboardButton(lang["audio.48"], callback_data='48')],
            [InlineKeyboardButton(lang["audio.49"], callback_data='49')],
            [InlineKeyboardButton(lang["audio.50"], callback_data='50')],
            [InlineKeyboardButton(lang["audio.51"], callback_data='51')],
            [InlineKeyboardButton(lang["audio.52"], callback_data='52')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Graphic Equalizers
    elif str(query.data) == str("48"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.53"], callback_data='53')],
            [InlineKeyboardButton(lang["audio.54"], callback_data='54')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Semi-parametric Equalizers
    elif str(query.data) == str("50"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.55"], callback_data='55')],
            [InlineKeyboardButton(lang["audio.56"], callback_data='56')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Parametric Equalizers
    elif str(query.data) == str("51"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.57"], callback_data='57')],
            [InlineKeyboardButton(lang["audio.58"], callback_data='58')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Speakers
    elif str(query.data) == str("6"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.59"], callback_data='59')],
            [InlineKeyboardButton(lang["audio.60"], callback_data='60')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Passive
    elif str(query.data) == str("59"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.61"], callback_data='61')],
            [InlineKeyboardButton(lang["audio.62"], callback_data='62')],
            [InlineKeyboardButton(lang["audio.63"], callback_data='63')],
            [InlineKeyboardButton(lang["audio.64"], callback_data='64')],
            [InlineKeyboardButton(lang["audio.65"], callback_data='65')],
            [InlineKeyboardButton(lang["audio.66"], callback_data='66')],
            [InlineKeyboardButton(lang["audio.67"], callback_data='67')],
            [InlineKeyboardButton(lang["audio.68"], callback_data='68')],
            [InlineKeyboardButton(lang["audio.69"], callback_data='69')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Active
    elif str(query.data) == str("60"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.70"], callback_data='70')],
            [InlineKeyboardButton(lang["audio.71"], callback_data='71')],
            [InlineKeyboardButton(lang["audio.72"], callback_data='72')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Headphones
    elif str(query.data) == str("7"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.73"], callback_data='73')],
            [InlineKeyboardButton(lang["audio.74"], callback_data='74')],
            [InlineKeyboardButton(lang["audio.75"], callback_data='75')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - On-ear
    elif str(query.data) == str("73"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.76"], callback_data='76')],
            [InlineKeyboardButton(lang["audio.77"], callback_data='77')],
            [InlineKeyboardButton(lang["audio.78"], callback_data='78')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Open-back(On-ear)
    elif str(query.data) == str("76"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.79"], callback_data='79')],
            [InlineKeyboardButton(lang["audio.80"], callback_data='80')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Semi-open-back(On-ear)
    elif str(query.data) == str("77"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.81"], callback_data='81')],
            [InlineKeyboardButton(lang["audio.82"], callback_data='82')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Closed-back(On-ear)
    elif str(query.data) == str("78"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.83"], callback_data='83')],
            [InlineKeyboardButton(lang["audio.84"], callback_data='84')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Over-ear
    elif str(query.data) == str("74"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.85"], callback_data='85')],
            [InlineKeyboardButton(lang["audio.86"], callback_data='86')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Open(Over-ear)
    elif str(query.data) == str("85"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.87"], callback_data='87')],
            [InlineKeyboardButton(lang["audio.88"], callback_data='88')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Closed(Over-ear)
    elif str(query.data) == str("86"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.89"], callback_data='89')],
            [InlineKeyboardButton(lang["audio.90"], callback_data='90')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - In-ear
    elif str(query.data) == str("75"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.91"], callback_data='91')],
            [InlineKeyboardButton(lang["audio.92"], callback_data='92')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Production Tools
    elif str(query.data) == str("8"):
        keyboard = [
            [
                InlineKeyboardButton(lang["audio.94"], callback_data='94'),
                InlineKeyboardButton(lang["audio.95"], callback_data='95'),
            ], [
                InlineKeyboardButton(lang["audio.96"], callback_data='96'),
            ], [
                InlineKeyboardButton(lang["audio.97"], callback_data='97'),
            ], [
                InlineKeyboardButton(lang["audio.98"], callback_data='98'),
                InlineKeyboardButton(lang["audio.99"], callback_data='99'),
            ], [
                InlineKeyboardButton(lang["audio.100"], callback_data='100'),
            ], [
                InlineKeyboardButton(lang["audio.101"], callback_data='101'),
            ], [
                InlineKeyboardButton(lang["audio.102"], callback_data='102'),
                InlineKeyboardButton(lang["audio.103"], callback_data='103'),
            ], [
                InlineKeyboardButton(lang["audio.104"], callback_data='104'),
                InlineKeyboardButton(lang["audio.105"], callback_data='105'),
            ], [
                InlineKeyboardButton(lang["audio.106"], callback_data='106'),
                InlineKeyboardButton(lang["audio.108"], callback_data='108'),
            ], [
                InlineKeyboardButton(lang["audio.109"], callback_data='109'),
            ], [
                InlineKeyboardButton(lang["audio.110"], callback_data='110'),
            ], [

                InlineKeyboardButton(lang["audio.0"], callback_data='0')
            ]]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Equalizers
    elif str(query.data) == str("104"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.111"], callback_data='111')],
            [InlineKeyboardButton(lang["audio.112"], callback_data='112')],
            [InlineKeyboardButton(lang["audio.113"], callback_data='113')],
            [InlineKeyboardButton(lang["audio.114"], callback_data='114')],
            [InlineKeyboardButton(lang["audio.115"], callback_data='115')],
            [InlineKeyboardButton(lang["audio.116"], callback_data='116')],
            [InlineKeyboardButton(lang["audio.117"], callback_data='117')],
            [InlineKeyboardButton(lang["audio.118"], callback_data='118')],
            [InlineKeyboardButton(lang["audio.119"], callback_data='119')],
            [InlineKeyboardButton(lang["audio.120"], callback_data='120')],
            [InlineKeyboardButton(lang["audio.121"], callback_data='121')],

            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Graphic Equalizers
    elif str(query.data) == str("113"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.122"], callback_data='122')],
            [InlineKeyboardButton(lang["audio.123"], callback_data='123')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Semi-parametric Equalizers
    elif str(query.data) == str("115"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.124"], callback_data='124')],
            [InlineKeyboardButton(lang["audio.125"], callback_data='125')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Parametric Equalizers
    elif str(query.data) == str("116"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.126"], callback_data='126')],
            [InlineKeyboardButton(lang["audio.127"], callback_data='127')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Accessories
    elif str(query.data) == str("9"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.128"], callback_data='128')],
            [InlineKeyboardButton(lang["audio.129"], callback_data='129')],
            [InlineKeyboardButton(lang["audio.130"], callback_data='130')],
            [InlineKeyboardButton(lang["audio.131"], callback_data='131')],
            [InlineKeyboardButton(lang["audio.132"], callback_data='132')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Go back to to main menu
    elif str(query.data) == str("0"):
        audio(update, context)


def tweet_profile_picture(update, context):
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_file.download("media/tweet/profile_picture_" +
                            update.message.from_user.name + ".jpg")
        update.message.reply_text(lang["tweet.step2"])
    except AttributeError:
        msg = update.message.text
        if msg == "/quit" or msg == "/quit@transpostingbot":
            update.message.reply_text(lang["tweet.exit"])
            return ConversationHandler.END
        update.message.reply_text(lang["tweet.invalid_file"])
        return None
    except IndexError:
        try:
            photo_file = update.message.sticker.get_file()
            photo_file.download('media/tweet/profile_picture_' +
                                update.message.from_user.name + ".jpg")
            try:
                sticker = Image.open(
                    "media/tweet/profile_picture_" + update.message.from_user.name + ".jpg")
            except IOError:
                update.message.reply_text(lang["tweet.invalid_file"])
                return None
            update.message.reply_text(lang["tweet.step2"])
        except AttributeError:
            msg = update.message.text
            if msg == "/quit" or msg == "/quit@transpostingbot":
                update.message.reply_text(lang["tweet.exit"])
                return ConversationHandler.END
            update.message.reply_text(lang["tweet.invalid_file"])
            return None
    return name


class TweetData:
    def __init__(self, name="", username=""):
        self.name = name
        self.username = username


user_data = dict()


def tweet_name(update, context):
    try:
        data = TweetData(str(update.message.text))
        user_data[update.message.from_user.id] = data
        # user_data["tweet_name_v"] = str(update.message.text)
        if user_data[update.message.from_user.id].name == "None":
            update.message.reply_text(lang["tweet.invalid_msg"])
            return None
        update.message.reply_text(lang["tweet.step3"])
    except AttributeError:
        update.message.reply_text(lang["tweet.invalid_msg"])
        return None
    return username


def tweet_username(update, context):
    try:
        data = TweetData(str(update.message.text))
        user_data[update.message.from_user.id].username = str(
            update.message.text)
        if user_data[update.message.from_user.id].username == "None":
            update.message.reply_text(lang["tweet.invalid_msg"])
            return None
        elif len(user_data[update.message.from_user.id].username) > 15:
            update.message.reply_text("Username too long")
            return None
        update.message.reply_text(lang["tweet.step4"])
    except AttributeError:
        update.message.reply_text(lang["tweet.invalid_msg"])
        return None
    return message


def tweet_exit(update, context):
    update.message.reply_text(lang["tweet.exit"])
    return ConversationHandler.END


def tweet_creator(update, context):
    # Get tweet message
    try:
        tweet_message_v = str(update.message.text)
        if tweet_message_v == "None":
            update.message.reply_text(lang["tweet.invalid_msg"])
            return None
    except AttributeError:
        update.message.reply_text(lang["tweet.invalid_msg"])
        return None

    if len(tweet_message_v) > 280:
        update.message.reply_text(lang["tweet.too_long"])
        return message

    def text_wrap(text, font, writing, max_width, max_height):
        lines = [[]]
        words = text.split()
        for word in words:
            lines[-1].append(word)
            (w, h) = writing.multiline_textsize(
                '\n'.join([' '.join(line) for line in lines]), font=font)
            if w > max_width:
                lines.append([lines[-1].pop()])
                (w, h) = writing.multiline_textsize(
                    '\n'.join([' '.join(line) for line in lines]), font=font)
                if h > max_height:
                    lines.pop()
                    lines[-1][-1] += '...'
                    while writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]),
                                                     font=font)[0] > max_width:
                        lines[-1].pop()
                        lines[-1][-1] += '...'
                    break
        return '\n'.join([' '.join(line) for line in lines])

    # Open tweet base image
    img = Image.open("media/tweet/tweet_base_1.png")
    draw = ImageDraw.Draw(img)
    # Fonts type
    font_type = "arial.ttf"
    font_type_bold = "arialbd.ttf"
    # Fonts
    name_font = ImageFont.truetype(font_type, 16)
    username_font = ImageFont.truetype(font_type_bold, 16)
    message_font = ImageFont.truetype(font_type, 24)
    date_font = ImageFont.truetype(font_type, 16)
    stats_font = ImageFont.truetype(font_type, 16)
    stats_font_bold = ImageFont.truetype(font_type_bold, 16)

    def mag_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000
        return '%.1f%s' % (num, ['', 'K'][magnitude])

    tweet_message_v_wrapped = text_wrap(
        tweet_message_v, message_font, draw, 430, 340)
    count = len(tweet_message_v_wrapped.splitlines())

    y = 140
    d_y = 85
    image_path = 0
    for i in range(count):
        y += 30
        d_y += 30
        image_path += 1

    # Write name, username, message and timestamp
    img = Image.open("media/tweet/tweet_base_" + str(image_path) + ".png")
    draw = ImageDraw.Draw(img)

    draw.text((86, 15), user_data[update.message.from_user.id].name,
              font=username_font, fill="white")

    draw.text((86, 38), "@" + user_data[update.message.from_user.id].username.replace(" ", "").replace("@", ""),
              font=name_font, fill="#8394a1")
    draw.text((26, 70), tweet_message_v_wrapped,
              font=message_font, fill="white")
    t = time.localtime()
    draw.text((27, d_y), time.strftime("%I:%M %p - %b %d, %Y", t),
              font=date_font, fill="#8394a1")

    # Retweets and Likes
    retweets = random.randint(1, 200000)
    likes = random.randint(1, 250000)
    retweets_readable = retweets
    likes_readable = likes
    if retweets >= 1000:
        retweets_readable = mag_format(retweets)
    if likes >= 1000:
        likes_readable = mag_format(likes)
    draw.text((27, y), str(retweets_readable),
              font=stats_font_bold, fill="white")

    if retweets <= 100:
        draw.text((50, y), "Retweets", font=stats_font, fill="#8394a1")
        draw.text((140, y), str(likes_readable),
                  font=stats_font_bold, fill="white")
        if likes <= 100:
            draw.text((163, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 1000:
            draw.text((173, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 10000:
            draw.text((178, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 100000:
            draw.text((188, y), "Likes", font=stats_font, fill="#8394a1")
        else:
            draw.text((198, y), "Likes", font=stats_font, fill="#8394a1")
    elif retweets <= 1000:
        draw.text((60, y), "Retweets", font=stats_font, fill="#8394a1")
        draw.text((150, y), str(likes_readable),
                  font=stats_font_bold, fill="white")
        if likes <= 100:
            draw.text((173, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 1000:
            draw.text((183, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 10000:
            draw.text((188, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 100000:
            draw.text((198, y), "Likes", font=stats_font, fill="#8394a1")
        else:
            draw.text((208, y), "Likes", font=stats_font, fill="#8394a1")
    elif retweets <= 10000:
        draw.text((65, y), "Retweets", font=stats_font, fill="#8394a1")
        draw.text((155, y), str(likes_readable),
                  font=stats_font_bold, fill="white")
        if likes <= 100:
            draw.text((178, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 1000:
            draw.text((188, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 10000:
            draw.text((193, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 100000:
            draw.text((203, y), "Likes", font=stats_font, fill="#8394a1")
        else:
            draw.text((213, y), "Likes", font=stats_font, fill="#8394a1")
    elif retweets <= 100000:
        draw.text((75, y), "Retweets", font=stats_font, fill="#8394a1")
        draw.text((165, y), str(likes_readable),
                  font=stats_font_bold, fill="white")
        if likes <= 100:
            draw.text((188, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 1000:
            draw.text((198, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 10000:
            draw.text((203, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 100000:
            draw.text((213, y), "Likes", font=stats_font, fill="#8394a1")
        else:
            draw.text((223, y), "Likes", font=stats_font, fill="#8394a1")
    else:
        draw.text((85, y), "Retweets", font=stats_font, fill="#8394a1")
        draw.text((175, y), str(likes_readable),
                  font=stats_font_bold, fill="white")
        if likes <= 100:
            draw.text((198, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 1000:
            draw.text((208, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 10000:
            draw.text((213, y), "Likes", font=stats_font, fill="#8394a1")
        elif likes <= 100000:
            draw.text((223, y), "Likes", font=stats_font, fill="#8394a1")
        else:
            draw.text((233, y), "Likes", font=stats_font, fill="#8394a1")

    # Generate round profile picture
    size = (256, 256)
    mask = Image.new('L', size, 0)
    draw_pf = ImageDraw.Draw(mask)
    draw_pf.ellipse((0, 0) + size, fill=255)
    pf = Image.open("media/tweet/profile_picture_" +
                    update.message.from_user.name + ".jpg")
    output_pf = ImageOps.fit(pf, mask.size, centering=(0.5, 0.5))
    output_pf.putalpha(mask)
    output_pf.save("media/tweet/round_profile_picture_" +
                   update.message.from_user.name + ".png")
    resize_pf = Image.open(
        "media/tweet/round_profile_picture_" + update.message.from_user.name + ".png")
    resize = (49, 49)
    resize_pf.thumbnail(resize)
    resize_pf.save("media/tweet/resized_pf_" +
                   update.message.from_user.name + ".png")

    # Save and send final tweet
    img.paste(resize_pf, (26, 10), resize_pf)
    img.save("media/tweet/tweet_" + update.message.from_user.name + ".png")
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open("media/tweet/tweet_" + update.message.from_user.name + ".png", "rb"))
    return ConversationHandler.END


# cmd handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
trans_handler = CommandHandler('trans', trans)
owo_handler = CommandHandler('owo', owo)
doggo_handler = CommandHandler('doggo', doggo)
spectral_handler = CommandHandler('spectral', spectral)
zalgo_handler = CommandHandler('zalgo', zalgos)
meme_handler = CommandHandler('meme', meme)
audio_handler = CommandHandler("audio", audio)
unsplash_handler = CommandHandler("unsplash", unsplash)
aouguri_handler = CommandHandler("aouguri", aouguri)
christmas_handler = CommandHandler("christmas", christmas)
pap_handler = CommandHandler("pap", pap)
slap_handler = CommandHandler("slap", slap)
inspire_handler = CommandHandler("inspire", inspire)

# conversation handlers
tweet_handler = ConversationHandler(
    entry_points=[CommandHandler('tweet', tweet_start)],
    states={
        PF: [MessageHandler(Filters.all, tweet_profile_picture)],
        name: [MessageHandler(Filters.all, tweet_name)],
        username: [MessageHandler(Filters.all, tweet_username)],
        message: [MessageHandler(Filters.all, tweet_creator)],
    },
    fallbacks=[CommandHandler('quit', tweet_exit)],
    per_user=True

)

# cmd dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(trans_handler)
dispatcher.add_handler(owo_handler)
dispatcher.add_handler(doggo_handler)
dispatcher.add_handler(spectral_handler)
dispatcher.add_handler(zalgo_handler)
dispatcher.add_handler(meme_handler)
dispatcher.add_handler(audio_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(audio_submenu))
dispatcher.add_handler(unsplash_handler)
dispatcher.add_handler(aouguri_handler)
dispatcher.add_handler(tweet_handler)
dispatcher.add_handler(christmas_handler)
dispatcher.add_handler(pap_handler)
dispatcher.add_handler(slap_handler)
dispatcher.add_handler(inspire_handler)

updater.start_polling()

print(colored(lang["bot.init_c"], "green"))
