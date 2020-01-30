# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from datetime import timedelta
from datetime import datetime
import json

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r') as f:
    phrases = json.load(f)

def check_day_time(t):
    if t.hour < metroTime["splitH"]:
        module = metroTime["MORNING"]
    else:
        module = metroTime["AFTERNOON"]
    return module

def check_input(data):
    data.strip()
    if len(data) <= 5 and data.count(':') == 1:
        times = data.split(':')
        if times[0].isdigit() and times[1].isdigit():
            if int(times[0]) >= 0 and int(times[0]) < 24:
                if int(times[1]) >= 0 and int(times[1]) < 60:
                    return True
    return False

def check_start(start, module):
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

def check_time(update, context, time):
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
        update.message.reply_text(tx, reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))
    return False

def get_time(stazione, start, end, time):
    module = check_day_time(time)
    t = timedelta(hours= time.hour, minutes= time.minute)
    t1 = check_start(start, module)
    delta = timedelta(minutes= module)
    toff = offset_test(end, stazione, t1)
    
    while toff < t:
        toff+= delta
    tx=""
    if(stazione.upper() != end.upper()):
        tx = str(stazione.upper())+" in direzione "+ str(end.upper()) +": " + ':'.join(str(toff).split(':')[:2])
    return tx

def get_metro_time(stazione, time):
    timeNes = get_time(stazione, "NESIMA", "STESICORO", time)
    timeSte = get_time(stazione, "STESICORO", "NESIMA", time)
    finalTime = timeNes+"\n"+timeSte
    return finalTime

def offset_test(end, stazione, t1):
    fine = "to"+end.upper()
    t1+=timedelta(minutes= metroTime[stazione.upper()][fine])
    return t1

def get_default_keyboard():
    reply_keyboard = [['🚇 Metro', '🚉 Stazioni', 'ℹ️ Info'],
                      ['👨‍💻 Chi siamo', '💙 Dona', '📢 Report'],
                      ['📜 Lista comandi']]
    return reply_keyboard