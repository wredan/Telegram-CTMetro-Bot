# -*- coding: utf-8 -*-

#bisogna inserire i valori del JSON metroTimetables, sto cercando di capire come navigarlo per estrarre i valori
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from datetime import timedelta
from datetime import datetime
import json

with open('metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

def offset(end, stazione, prevH, prevM):
    fine = "to"+end.upper()
    prevM+=metroTime[staz].
    tx = "La prossima metro da "+str(stazione.upper())+" in direzione "+ str(end.upper()) +" è alle: " + str(prevH) + ":" + str(prevM)
    return tx

def getMetroTime(stazione, start, end):
    if start == "NESIMA":
        t1 = timedelta(hours = 6, minutes= 40)
    else:
        t1 = timedelta(hours = 7, minutes= 0)
    t = datetime.now()
    t3 = t - t1
    m = (t.hour * 60) + t.minute
    minutes = (t3.hour * 60) + t3.minute
    prevTime = m + (10 - (minutes % 10))
    prevH = prevTime // 60
    prevMin = prevTime % 60
    return offset(end, stazione, prevH, prevMin)

def getMetro(bot, update):
    mex = update.message.text
    timeNes = getMetroTime(mex[7:], "NESIMA", "STESICORO")
    timeSte = getMetroTime(mex[7:], "STESICORO", "NESIMA")
    chat_id = update.message.chat_id
    time = timeNes+"\n"+timeSte
    bot.send_message(chat_id=chat_id, text= time)
    
