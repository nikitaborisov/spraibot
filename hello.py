from slackbot.bot import respond_to
import re
import random

welcomes = [
"You're welcome",
"My pleasure",
"No problem",
"Not at all",
"De nada",
"No worries",
"Anytime",
"Don't mention it",
"Sure thing"
]

@respond_to("Hello", re.IGNORECASE)
def hello(message):
    message.reply("Hello, {}!".format(message.user["profile"]["first_name"]))

@respond_to("Thank(\s+you|s)", re.IGNORECASE)
def thanks(message, _):
    message.reply("{}, {}!".format(random.choice(welcomes),
        message.user["profile"]["first_name"]))
