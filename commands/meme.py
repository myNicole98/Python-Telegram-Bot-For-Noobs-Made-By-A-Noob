import random, praw, json

# Load credentials
with open("credentials.json", "r") as f:
    credentials = json.load(f)

def meme(update, context):

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