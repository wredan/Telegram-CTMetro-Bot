# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CallbackContext
from datetime import datetime, timedelta
from Modules.Keyboard import *
from Settings import *
import time
import pytz

tz = pytz.timezone('Europe/Rome')

STAZIONE, ORARIO, SCEGLIORARIO = range(3)

def get_stazione(update, context: CallbackContext):
    reply_keyboard = []
    for el in metroTime["STAZIONI"]:
        reply_keyboard.append([el])
    update.message.reply_text(' 🚇 Scegli una stazione (sono ordinate da NESIMA a STESICORO).\n\n Digita /cancella per terminare la richiesta', 
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    return STAZIONE

def get_orario(update, context: CallbackContext):
    text = update.message.text
    if '/' in text:
        update.message.reply_text('Stazione non accettata, non inserire comandi, attieniti alle stazioni indicate sotto nei pulsanti.')
        return STAZIONE
    elif text not in metroTime["STAZIONI"]:
        update.message.reply_text('Stazione non accettata, attieniti alle stazioni indicate sotto nei pulsanti.')
        return STAZIONE
    else:
        context.user_data["Stazione"] = update.message.text
        update.message.reply_text('🕓 Bene, a che ora ti interessa sapere la prossima metro?\n\n Digita /cancella per terminare la richiesta',
            reply_markup=ReplyKeyboardMarkup(get_scelta_orario_keyboard(), resize_keyboard=True))
        return ORARIO

def get_next_metro(update, context: CallbackContext):
    tx = update.message.text.strip()    
    if tx == "Adesso":
        x = datetime.now(tz)
        if check_time(update, context, x):
            final_time = get_metro_time(context.user_data["Stazione"], x)
            update.message.reply_text(final_time, reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))
        return ConversationHandler.END
    elif tx == "Scegli orario":
        update.message.reply_text('Srivi un orario (formato hh:mm) per il quale vuoi sapere la prossima metro disponibile.\n\n Digita /cancella per terminare la richiesta',
        reply_markup= ReplyKeyboardRemove())
        return SCEGLIORARIO
    else:
        update.message.reply_text('Scelta non valida, attieniti alle opzioni presenti in tastiera.\n\n Digita /cancella per terminare la richiesta')        
        return ORARIO   
    
def scegli_orario(update, context: CallbackContext):
    tx = update.message.text.strip()
    x = datetime.now(tz)
    if check_input(tx) and tx != "":
        time = tx.split(':')
        t = datetime(x.year, x.month, x.day, int(time[0]), int(time[1]))
        if check_time(update, update, t):
            final_time = get_metro_time(context.user_data["Stazione"], t)
            update.message.reply_text(final_time, reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))
        return ConversationHandler.END
    else:
        update.message.reply_text('Formato dell\'ora non valido, il formato accettato è hh:mm')        
        return SCEGLIORARIO

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
        tx = "🚈 " + str(stazione.upper())+" ➡️ "+ str(end.upper()) +": " + ':'.join(str(toff).split(':')[:2])
    return tx

def get_metro_time(stazione, time):
    timeNes = get_time(stazione, "NESIMA", "STESICORO", time)
    timeSte = get_time(stazione, "STESICORO", "NESIMA", time)
    finalTime = timeNes+"\n\n"+timeSte
    return finalTime

def offset_test(end, stazione, t1):
    fine = "to"+end.upper()
    t1+=timedelta(minutes= metroTime[stazione.upper()][fine])
    return t1