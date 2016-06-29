from slackbot.bot import listen_to, respond_to
import re
import shelve
import dateutil.parser
import datetime
import json

deadlines = shelve.open('deadlines', writeback=True)
if "list" not in deadlines:
    deadlines["list"] = []

@respond_to(r'(.*) on (.*)', re.IGNORECASE)
def set_deadline(message, item, datestr):
    try:
        date = dateutil.parser.parse(datestr)
    except:
        return  # can't parse so ignore the date
    today = datetime.datetime.today()
    if date < today:
        if date.year == today.year:
            date = date.replace(year=date.year+1)
        else:
            return  # too far in the past
    deadlines["list"].append((date,item))
    deadlines.sync()
    message.reply("Set deadline: {} is on {}".format(item, date.strftime("%b %d, %Y")))

@respond_to(r'deadlines', re.IGNORECASE)
def list_deadlines(message):
    attachments = []
    for date,item in sorted(deadlines["list"]):
        d = (date - datetime.datetime.today()).days + 1
        if d < 0:
            continue
        attach = {"mrkdwn_in": ["text"]}
        if d > 1:
            attach["text"] = "{} days until {}".format(d,item)
        elif d == 1:
            attach["text"] = "*{} tomorrow!*".format(item)
        else:
            attach["text"] = "*{} TODAY!*".format(item)
            attach["color"] = "#ff0000"
        if d < 7 and d > 0:
            attach["color"] = "#ffff00"
        attachments.append(attach)
    if attachments:
        message.send_webapi('', json.dumps(attachments))
    else:
        message.reply("No deadlines!")







        
