# -*- coding: utf-8 -*-

from datetime import timedelta
from datetime import datetime
import json

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r') as f:
    phrases = json.load(f)

def checkDayTime(t):
    if t.hour < metroTime["splitH"]:
        module = metroTime["MORNING"]
    else:
        module = metroTime["AFTERNOON"]
    return module

def checkInput(data):
    data.strip()
    if len(data) <= 5 and data.count(':') == 1:
        times = data.split(':')
        if times[0].isdigit() and times[1].isdigit():
            if times[0] >= '0' and times[0] < '24':
                if times[1] >= '0' and times[1] < '60':
                    return True
    return False

def checkStart(start, module):
    if start == "NESIMA":
        if module != 15:
            t = timedelta(hours = metroTime["startNesimaMattina"]["hour"], minutes= metroTime["startNesimaMattina"]["minutes"])
        else:
            t = timedelta(hours = metroTime["startNesimaPomeriggio"]["hour"], minutes= metroTime["startNesimaPomeriggio"]["minutes"])
    else:
        if module != 15:
            t = timedelta(hours = metroTime["startStesicoroMattina"]["hour"], minutes= metroTime["startStesicoroMattina"]["minutes"])
        else:
            t = timedelta(hours = metroTime["startStesicoroPomeriggio"]["hour"], minutes= metroTime["startStesicoroPomeriggio"]["minutes"])   
    return t

def checkTime(bot, update, time):
    t = time
    if t.hour > metroTime["startServiceHour"] and t.hour <= metroTime["endService"] - 1:
        return True
    elif t.hour == metroTime["startServiceHour"] and t.minute>=["startServiceMinute"]:
        return True
    else:
        startNesimaH = metroTime["startNesimaMattina"]["hour"]
        startNesimaM = metroTime["startNesimaMattina"]["minutes"]
        startStesicoroH = metroTime["startStesicoroMattina"]["hour"]
        startStesicoroM = metroTime["startStesicoroMattina"]["minutes"]
        tx = "Servizio sospeso\n"
        tx+= "Il primo treno disponibile da NESIMA: " + str(startNesimaH) +":"+ str(startNesimaM) +"\n"
        tx+= "Il primo treno disponibile da STESICORO: " + str(startStesicoroH) +":"+ str(startStesicoroM) + "0" 
        bot.send_message(chat_id= update.message.chat_id, text= tx)
        return False

def getMetroTime(stazione, start, end, time):
    module = checkDayTime(time)
    t = timedelta(hours= time.hour, minutes= time.minute)
    t1 = checkStart(start, module)
    delta = timedelta(minutes= module)
    toff = offsetTest(end, stazione, t1)
    while toff < t:
        toff+= delta
    tx=""
    if(stazione.upper() != end.upper()):
        tx = str(stazione.upper())+" in direzione "+ str(end.upper()) +": " + ':'.join(str(toff).split(':')[:2])
    return tx

def getTime(stazione, time):
    timeNes = getMetroTime(stazione, "NESIMA", "STESICORO", time)
    timeSte = getMetroTime(stazione, "STESICORO", "NESIMA", time)
    finalTime = timeNes+"\n"+timeSte
    return finalTime

def offsetTest(end, stazione, t1):
    fine = "to"+end.upper()
    t1+=timedelta(minutes= metroTime[stazione.upper()][fine])
    return t1