# -*- coding: utf-8 -*-

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from datetime import timedelta
from datetime import datetime
import json

with open('metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

def offset(end, stazione, prevH, prevM):
    fine = "to"+end.upper()
    prevM+=metroTime[stazione.upper()][fine]
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

def checkMessage(message, bot, chat_id):
    if message.count(' ') == 1 and len(message) > 7:
        return True
    else:
        mex = "Inserisci un testo del tipo: /metro <nome stazione>"
        bot.send_message(chat_id=chat_id, text= mex)
    return False


def getMetro(bot, update):
    mex = update.message.text
    chat_id = update.message.chat_id
    if checkMessage(mex, bot, chat_id):
        timeNes = getMetroTime(mex[7:], "NESIMA", "STESICORO")
        timeSte = getMetroTime(mex[7:], "STESICORO", "NESIMA")
        time = timeNes+"\n"+timeSte
        bot.send_message(chat_id=chat_id, text= time)        

def getInfo(bot, update):
    info = """Il bot permette di ricevere delle informazioni sulla prossima metro disponibile nella stazione indicata ad esempio da una stringa del tipo:
    /metro <nome stazione>
    Esempio: /metro milo
    Il bot è stato costruito senza la collaborazione della Ferrovia Circumetnea, quindi i dati qui presenti sono frutto di una misurazione manuale dei tempi di percorrenza. Sono quindi da prendere come una indicazione e non come un orario esatto.
    Siamo comunque ben disponibili a collaborazioni con l'azienda per aumentare la precisione di questi orari."""
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text= info) 
    
