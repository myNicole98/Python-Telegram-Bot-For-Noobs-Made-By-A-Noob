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
import owoify
from uuid import uuid4
import warnings
import requests
import urllib
import random
import pylab
import wave
import praw
import time
import os
import gc

import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    #log(update, lang["spectral.log"])

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

        print("audio scaricato")

        # Convert audio to mono wav
        sound = AudioSegment.from_file("media/audio/audio.file")
        sound = sound.set_channels(1)
        sound.export("media/audio/audio.wav", format="wav")

        print("audio convertito")

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