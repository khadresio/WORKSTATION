import logging
import os
import subprocess
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep


update_id = None

def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('TOKEN')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
	    #resp=os.system("sudo python wit2.py "+update.message.text)
            proc = subprocess.Popen("sudo python wit2.py '"+update.message.text+"'", stdout=subprocess.PIPE,shell=True)
            resp= proc.stdout.read()
            update.message.reply_text(resp)


if __name__ == '__main__':
    main()

