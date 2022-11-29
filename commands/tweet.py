from localization.localization import lang
from PIL import Image, ImageFont, ImageDraw, ImageOps
from telegram.ext import ConversationHandler
import random, time

PF, name, username, message, done, tquit = range(6)

def tweet_start(update, context):

    update.message.reply_text(lang["tweet.step1"])
    return PF

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