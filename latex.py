from urllib.parse import quote
from html import unescape
from slackbot.bot import listen_to, respond_to
import json

@listen_to(r'^\$(.*)\$$')
@respond_to(r'^\$(.*)\$$')
def render_latex(message, latex):
    # based on https://github.com/nicolewhite/SlackTeX/blob/master/slacktex/views.py
    latex_url = "http://chart.apis.google.com/chart?cht=tx&chl={latex}".format(
        latex=quote(unescape(latex)))
    message.send_webapi('', json.dumps([{"image_url": latex_url,
        "fallback": "Latex rendering fail?"}]))
