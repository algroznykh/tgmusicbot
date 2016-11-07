#coding = utf-8

import subprocess
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler

# get CMUSICBOT_KEY via botfather bot
SOMAFM_TEMPLATE = 'http://somafm.com/{}.pls'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

updater=Updater(token=CMUSICBOT_KEY) 
dispatcher = updater.dispatcher

class Player:
    player = None

p = Player()

def somafm(bot, update, **args):
    name = args.get('args')
    if not name:
        bot.sendMessage(chat_id=update.message.chat_id, text="select station".format([update, args]))
    else:
        station(name[0])

def halp(bot, update, *args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Friends can halp")

def station(name):
    soma_url = SOMAFM_TEMPLATE.format(name)
    if p.player:
        p.player.kill()
        p.player = None
    p.player = subprocess.Popen(["vlc", "-I", "dummy", soma_url])

somafm_handler = CommandHandler('somafm', somafm, pass_args=True)
halp_handler = CommandHandler('halp', halp)

dispatcher.add_handler(somafm_handler)
dispatcher.add_handler(halp_handler)

if __name__ == '__main__':
  updater.start_polling()
