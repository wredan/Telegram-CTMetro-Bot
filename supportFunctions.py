# -*- coding: utf-8 -*-

from datetime import timedelta
from datetime import datetime
import json

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r') as f:
    phrases = json.load(f)

def checkDayTime():
    t = datetime.now()
    if t.hour < metroTime["splitH"]:
        module = metroTime["MORNING"]
    else:
        module = metroTime["AFTERNOON"]
    return module

def checkStation(message, bot, chat_id):
    if len(message) > 7:
        for el in metroTime["STAZIONI"]:
            if message[7:].upper() == el:
                return True
        mex = phrases["noStations"]
        bot.send_message(chat_id=chat_id, text= mex)
        return False
    else:
        mex = phrases["errStations"]
        bot.send_message(chat_id=chat_id, text= mex)
    return False

def checkTime(bot, chat_id):
    #TODO: controlla cosa ti ritorna datetime.now()
    t = datetime.now()
    if t.hour > metroTime["startServiceHour"] and t.hour <= metroTime["endService"] - 1:
        return True
    else if t.hour == metroTime["startServiceHour"] and t.minute>=["startServiceMinute"]:
        return True
    else:
        startNesimaH = metroTime["startNesima"]["hour"]
        startNesimaM = metroTime["startNesima"]["minutes"]
        startStesicoroH = metroTime["startStesicoro"]["hour"]
        startStesicoroM = metroTime["startStesicoro"]["minutes"]
        tx = "Servizio sospeso\n"
        tx+= "Il primo treno disponibile da NESIMA: " + str(startNesimaH) +":"+ str(startNesimaM) +"\n"
        tx+= "Il primo treno disponibile da STESICORO: " + str(startStesicoroH) +":"+ str(startStesicoroM) + "0"
        bot.send_message(chat_id=chat_id, text= tx)
        return False

def getMetroTime(stazione, start, end):
    t = datetime.now()
    if start == "NESIMA":
        t1 = timedelta(hours = 6, minutes= 40)
    else:
        t1 = timedelta(hours = 7, minutes= 0)
    module = checkDayTime()
    t3 = t - t1
    m = (t.hour * 60) + t.minute
    minutes = (t3.hour * 60) + t3.minute
    prevTime = m + (module - (minutes % module))
    prevH = prevTime // 60
    prevMin = prevTime % 60
    return offset(end, stazione, prevH, prevMin)
    
def offset(end, stazione, prevH, prevM):
    fine = "to"+end.upper()
    prevM+=metroTime[stazione.upper()][fine]
    module = checkDayTime()
    if prevM//module == 0:
        prevM = "0"+str(prevM%60)
    tx = "metro da "+str(stazione.upper())+" verso "+ str(end.upper()) +": " + str(prevH) + ":" + str(prevM)
    return tx