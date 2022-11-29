def pap(update, context):

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