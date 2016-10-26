from slackbot.bot import listen_to, respond_to
import re
import dateutil.parser
import datetime
import json
from db import Deadline
import db

session = db.Session()


@respond_to(r'(.*)(\s+is)?\s+on\s+(.*)', re.IGNORECASE)
def set_deadline(message, item, _, datestr):
    try:
        date = dateutil.parser.parse(datestr).date()
    except:
        return  # can't parse so ignore the date
    today = datetime.date.today()
    if date < today:
        if date.year == today.year:
            date = date.replace(year=date.year + 1)
        else:
            return  # too far in the past
    d = Deadline(date=date, item=item)
    session.add(d)
    session.commit()
    datestr = date.strftime("%b %d, %Y")
    message.reply("Set deadline: {} is on {}".format(item, datestr))


@listen_to(r'^deadlines?', re.IGNORECASE)
@respond_to(r'deadlines?', re.IGNORECASE)
def list_deadlines(message):
    attachments = []
    for deadline in session.query(Deadline).order_by(Deadline.date):
        days = (deadline.date - datetime.date.today()).days
        if days < 0:
            continue
        attach = {"mrkdwn_in": ["text"]}
        if days > 1:
            attach["text"] = "{} days until {}".format(days, deadline.item)
        elif days == 1:
            attach["text"] = "*{} tomorrow!*".format(deadline.item)
        else:
            attach["text"] = "*{} TODAY!*".format(deadline.item)
            attach["color"] = "#ff0000"
        if days < 7 and days > 0:
            attach["color"] = "#ffff00"
        attachments.append(attach)
    if attachments:
        message.send_webapi('', json.dumps(attachments))
    else:
        message.reply("No deadlines!")


@respond_to('forget(\s+about)?\s+(.*)', re.IGNORECASE)
def forget_deadline(message, _, match):
    if '%' not in match:
        match += '%'   # prefix search
    q = list(session.query(Deadline).filter(Deadline.item.like(match)))
    if not q:
        message.reply("No matching deadlines")
    elif len(q) > 1:
        message.reply("More than one matching deadline: {}".format(x.item
                                                                   for x in q))
    else:
        message.reply("Deleting deadline {}".format(q[0].item))
        session.delete(q[0])
        session.commit()
