from localization.localization import lang
from pydub import AudioSegment
from telegram.error import BadRequest
import os, gc

def spectral(update, context):

    extensions = ("m4a", "mp3", "wav", "flac")
    try:
        # Get file
        try:
            message = update.message.reply_to_message.audio.get_file()
        except AttributeError:
            message = update.message.reply_to_message.document.get_file()
        if any(x in str(extensions) for x in str(message)):
            pass
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                        text=lang["spectral.invalid"])
            return None
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
                    "spectrogram -x 1920 -Y 1080 -o media/spectrogram/spectrogram.png")

        # Send album
        context.bot.send_document(chat_id=update.effective_chat.id,
                                    reply_to_message_id=update.message.reply_to_message.message_id,
                                    document=open("media/spectrogram/spectrogram.png", "rb"))
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