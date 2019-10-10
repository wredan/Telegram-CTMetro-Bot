# -*- coding: utf-8 -*-

from datetime import timedelta
from datetime import datetime
import json

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r' ,errors='ignore') as f:
    phrases = json.load(f)

def checkDayTime():
    t = datetime.now()
    if t.hour < metroTime["splitH"]:
        module = metroTime["MORNING"]
    else:
        module = metroTime["AFTERNOON"]
    return module

def checkStart(start):
    if start == "NESIMA":
        t = timedelta(hours = metroTime["startNesima"]["hour"], minutes= metroTime["startNesima"]["minutes"])
    else:
        t = timedelta(hours = metroTime["startStesicoro"]["hour"], minutes= metroTime["startStesicoro"]["minutes"])
    return t

def checkTime(bot, query):
    #todo: controlla cosa ti ritorna datetime.now()
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
    t = time
    print(t.strftime("%H:%M:%S"))
    t1 = checkStart(start)
    # print(t1.strftime("%H:%M:%S"))
    module = checkDayTime()
    delta = timedelta(minutes= module)
    # print(module.strftime("%H:%M:%S"))
    while t1 < t:
        t1+= delta
    return offsetTest(end, stazione, t1)
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
    
def offset(end, stazione, prevH, prevM):
    fine = "to"+end.upper()
    prevM+=metroTime[stazione.upper()][fine]
    module = checkDayTime()
    if prevM//module == 0:
        prevM = "0"+str(prevM%60)
    tx=""
    if(stazione.upper() != end.upper()):
        tx = "metro da "+str(stazione.upper())+" verso "+ str(end.upper()) +": " + str(prevH) + ":" + str(prevM) + " sono le " + datetime.now().strftime("%H:%M:%S")
    return tx

def offsetTest(end, stazione, t1):
    fine = "to"+end.upper()
    offset = timedelta(minutes= metroTime[stazione.upper()][fine])
    t1+=offset
    tx=""
    if(stazione.upper() != end.upper()):
        tx = "metro da "+str(stazione.upper())+" verso "+ str(end.upper()) +": " + t1.strftime("%H:%M") + " sono le " + datetime.now().strftime("%H:%M:%S")
    return tx