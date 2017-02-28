#coding = utf-8
from telegram.ext import Updater
from telegram.ext import CommandHandler

from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup

import subprocess

import logging

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
        song = get_song()
        keyboard = [[InlineKeyboardButton("/songname")]]
        station(name[0])
        bot.sendMessage(chat_id=update.message.chat_id, text="{}: {}".format(name[0], song), 
                        reply_markup=keyboard)

def halp(bot, update, *args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Friends can halp")

def station(name):
    soma_url = SOMAFM_TEMPLATE.format(name)
    if p.player:
        stop()
    p.station = name
    p.player = subprocess.Popen(["vlc", "-I", "dummy", soma_url])

def volume(bot, update, **args):
    level = args.get("args")
    command = ["amixer", "sset", "PCM", "{}%".format(level[0])]
    print("COMMAND: {}".format(" ".join(command)))
    subprocess.Popen(command)

def whoshome(bot, update):
    pass

def youtube(bot, update, **args):
    stop()
    u = args.get("args")[0]
    command = ["mpsyt", "playurl", u]
    p.player = subprocess.Popen(command)

def speak(bot, update, **args):
    phrase = args.get("args")
    subprocess.Popen(["espeak", "--", ",".join(phrase)])

def get_song():
    command = 'curl -s somafm.com/{}/ | grep "Now Playing" | cut -d ">" -f 3'.format(p.station)
    song = subprocess.getoutput(command)
    return song

def songname(bot, update):
    song = get_song()
    bot.sendMessage(chat_id=update.message.chat_id, text="{}: {}".format(p.station, song))

def stop(*_):
    if p.player:
        p.player.kill()
    p.player = None

def resume(*_):
    if p.station:
        station(p.station)

somafm_handler = CommandHandler('somafm', somafm, pass_args=True)
espeak_handler = CommandHandler('speak', speak, pass_args=True)
volume_handler = CommandHandler('volume', volume, pass_args=True)
songname_handler = CommandHandler('songname', songname)
stop_handler = CommandHandler('stop', stop)
resume_handler = CommandHandler('play', resume)
url_handler = CommandHandler('youtube', youtube, pass_args=True)

halp_handler = CommandHandler('halp', halp)

dispatcher.add_handler(somafm_handler)
dispatcher.add_handler(halp_handler)
dispatcher.add_handler(espeak_handler)
dispatcher.add_handler(songname_handler)
dispatcher.add_handler(volume_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(resume_handler)
dispatcher.add_handler(url_handler)

updater.start_polling()

def read_button():
    import serial
    s = serial.Serial('/dev/ttyACM0', 9600)
    while True:
        b = s.read_all()
        if b and b[-1] == 1:
            logging.info('button was pressed')
            if p.player:
                stop()
            else:
                resume()
read_button()
