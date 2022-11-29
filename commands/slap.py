def slap(update, context):

    try:
        msg = update.message.reply_to_message

        # Write user id on database
        slap_dtb = open("media/slap/slap.txt", "a")
        user_id = update.message.reply_to_message.from_user.id
        if (user_id == 78679195):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="I can't slap my own creator uwu")
        else:
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