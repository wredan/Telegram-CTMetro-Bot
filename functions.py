# -*- coding: utf-8 -*-

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from supportFunctions import *
import json

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r') as f:
    phrases = json.load(f)

def getMetro(bot, update):
    mex = update.message.text
    chat_id = update.message.chat_id
    if checkStation(mex, bot, chat_id) and checkTime(bot, chat_id):
        timeNes = getMetroTime(mex[7:], "NESIMA", "STESICORO")
        timeSte = getMetroTime(mex[7:], "STESICORO", "NESIMA")
        time = timeNes+"\n"+timeSte
        bot.send_message(chat_id=chat_id, text= time)        

def getInfo(bot, update):
    info = phrases["info"]
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text= info) 

def getChatId(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= chat_id)
    
def getAuthor(bot, update):
    aut = phrases["author"]
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= aut)

def startBot(bot, update):
    st = phrases["start"]
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= st)

def getStazioni(bot, update):
    mex = ""
    for el in metroTime["STAZIONI"]:
        mex+=el+"\n"
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= mex)
