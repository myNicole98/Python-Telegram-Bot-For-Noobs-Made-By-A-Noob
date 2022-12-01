from localization.localization import lang
import urllib, os
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap

def unsplash(update, context):

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

    font_type = "fnt/sans-jp-emojionecolor_merged.ttf"
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
                draw_interface.text((100, 920),
                                    "- " + username,
                                    font=fontquote,
                                    fill="white", stroke_width=3, stroke_fill="black", embedded_color=True)
            except AttributeError:
                draw_interface.text((100, 920), "- " + str(update.message.reply_to_message.from_user.full_name),
                                    font=fontquote,
                                    fill="white", stroke_width=3, stroke_fill="black", embedded_color=True)

        # Save image and send it
        img.save('media/unsplash/unsplash.png')
        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open("media/unsplash/unsplash.png", "rb"),
                                reply_to_message_id=update.message.reply_to_message.message_id)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lang["unsplash.too_long"])