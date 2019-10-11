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

def checkTime(bot, query):
    t = datetime.now()
    if t.hour > metroTime["startServiceHour"] and t.hour <= metroTime["endService"] - 1:
        return True
    elif t.hour == metroTime["startServiceHour"] and t.minute>=["startServiceMinute"]:
        return True
    else:
        startNesimaH = metroTime["startNesima"]["hour"]
        startNesimaM = metroTime["startNesima"]["minutes"]
        startStesicoroH = metroTime["startStesicoro"]["hour"]
        startStesicoroM = metroTime["startStesicoro"]["minutes"]
        tx = "Servizio sospeso\n"
        tx+= "Il primo treno disponibile da NESIMA: " + str(startNesimaH) +":"+ str(startNesimaM) +"\n"
        tx+= "Il primo treno disponibile da STESICORO: " + str(startStesicoroH) +":"+ str(startStesicoroM) + "0"
        query.edit_message_text(text= tx)
        return False

def getMetroTime(stazione, start, end, time):
    t = timedelta(hours= time.hour, minutes= time.minute)
    module = checkDayTime()
    t1 = checkStart(start, module)
    delta = timedelta(minutes= module)
    toff = offsetTest(end, stazione, t1)
    while toff < t:
        toff+= delta
    tx=""
    if(stazione.upper() != end.upper()):
        tx = str(stazione.upper())+" in direzione "+ str(end.upper()) +": " + ':'.join(str(toff).split(':')[:2])
    return tx

def offsetTest(end, stazione, t1):
    fine = "to"+end.upper()
    t1+=timedelta(minutes= metroTime[stazione.upper()][fine])
    return t1

#tutto quello sotto potenzialmente non serve ad un cazzo (:
    #t3 = t - t1
    #print(t3.strftime("%H:%M:%S"))
    #m = (t.hour * 60) + t.minute
    #minutes = (t3.hour * 60) + t3.minute
    #prevTime = m + (module - (minutes % module))
    #prevH = prevTime // 60
    #prevMin = prevTime % 60
    #return offset(end, stazione, prevH, prevMin)

# def getMetroTime(stazione, start, end):
#     t = datetime.now()
#     t1 = checkStart(start)
#     module = checkDayTime()
#     t3 = t - t1
#     m = (t.hour * 60) + t.minute
#     minutes = (t3.hour * 60) + t3.minute
#     prevTime = m + (module - (minutes % module))
#     prevH = prevTime // 60
#     prevMin = prevTime % 60
#     return offset(end, stazione, prevH, prevMin)
    
#def offset(end, stazione, prevH, prevM):
#    fine = "to"+end.upper()
#    prevM+=metroTime[stazione.upper()][fine]
#    module = checkDayTime()
#    if prevM//module == 0:
#        prevM = "0"+str(prevM%60)
#    tx=""
#    if(stazione.upper() != end.upper()):
#        tx = "metro da "+str(stazione.upper())+" verso "+ str(end.upper()) +": " + str(prevH) + ":" + str(prevM) + " sono le " + datetime.now().strftime("%H:%M:%S")
#    return tx