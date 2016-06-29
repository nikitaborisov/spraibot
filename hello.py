from slackbot.bot import respond_to
import re

@respond_to("Hello", re.IGNORECASE)
def hello(message):
    message.reply("Hello, {}!".format(message.user["profile"]["first_name"]))
