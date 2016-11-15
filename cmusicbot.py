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
    station = None

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
    p.station = name
    p.player = subprocess.Popen(["vlc", "-I", "dummy", soma_url])
    
def speak(bot, update, **args):
    phrase = args.get("args")
    subprocess.Popen(["espeak", "--", ",".join(phrase)])

def songname(bot, update):
    command = 'curl -s somafm.com/{}/ | grep "Now Playing" | cut -d ">" -f 3'.format(p.station)
    song = subprocess.getoutput(command)
    bot.sendMessage(chat_id=update.message.chat_id, text="{}: {}".format(p.station, song))

somafm_handler = CommandHandler('somafm', somafm, pass_args=True)
espeak_handler = CommandHandler('speak', speak, pass_args=True)
songname_handler = CommandHandler('songname', songname)

halp_handler = CommandHandler('halp', halp)

dispatcher.add_handler(somafm_handler)
dispatcher.add_handler(halp_handler)
dispatcher.add_handler(espeak_handler)
dispatcher.add_handler(songname_handler)

updater.start_polling()
