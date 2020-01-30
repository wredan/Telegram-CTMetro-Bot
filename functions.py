# -*- coding: utf-8 -*-

from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CallbackContext
from datetime import datetime
from supportFunctions import *
import json
import time
import os
import sys
import pytz
import logging

with open('./jsonFiles/metroTimetables.json', 'r',errors='ignore') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r', errors='ignore') as f:
    phrases = json.load(f)

with open('./config/config.json', 'r', errors='ignore') as f:
    config_get = json.load(f)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

sleepTime = 0.200
tz = pytz.timezone('Europe/Rome')

STAZIONE, ORARIO, SCEGLIORARIO = range(3)

REPMESSAGE = range(1)

def callback(update, context):
    query = update.callback_query
    if str(query.data) == "clearReportFile":
        f = open("./data/reports.txt", "w")
        f.write('')
        f.close()
        query.edit_message_text(text= "File ripulito correttamente")
    elif str(query.data) == "none":
        query.edit_message_text(text= "Operazione annullata")
    else:
        data = query.data.split('-')
        x = datetime.now(tz)
        if data[1] != "/metro":
            orario = data[1].split(':')
            x = datetime(x.year, x.month, x.day, int(orario[0]), int(orario[1]))
        time = getTime(data[0], x)
        query.edit_message_text(text= time)

def clearReports(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        keyboard = [[InlineKeyboardButton("Si", callback_data='clearReportFile'), InlineKeyboardButton("No", callback_data='none')]]
        update.message.reply_text('Sicuro di voler eliminare tutti i report?', reply_markup=InlineKeyboardMarkup(keyboard))

def donate(update, context):
    update.message.reply_text(text= phrases["donate"])

def get_author(update, context):
    update.message.reply_text(text= phrases["chiSiamo"])

def get_chat_id(update, context):
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id= chat_id, text= chat_id)

def get_lista_comandi(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        context.bot.sendMessage(chat_id= chat_id, text= phrases["commandsList"])
    else:
        get_help(update, update)

def get_help(update, context):
    update.message.reply_text(text= phrases["help"])

def get_info(update, context):
    update.message.reply_text(text= phrases["info"])

def get_stazione(update, context: CallbackContext):
    reply_keyboard = []
    for el in metroTime["STAZIONI"]:
        reply_keyboard.append([el])
    update.message.reply_text('Scegli una stazione (sono ordinate da NESIMA a STESICORO).\n\n Digita /cancella per terminare la richiesta', 
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

    return STAZIONE

def get_orario(update, context: CallbackContext):
    reply_keyboard = [['Adesso', 'Scegli orario']]
    context.user_data["Stazione"] = update.message.text
    update.message.reply_text(
        'Bene, a che ora ti interessa sapere la prossima metro?\n\n Digita /cancella per terminare la richiesta',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
    
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

    
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Arrivederci, a presto!',
                              reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))
    return ConversationHandler.END

def get_stazioni(update, context):
    mex = ""
    for el in metroTime["STAZIONI"]:
        mex+="🚉 "+ el + "\n\n"
    update.message.reply_text(mex)        

def writeOnReportsFile(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        tx = update.message.text
        if len(tx) > 14:
            f = open("./data/reports.txt", "w")
            f.write(tx[14:])
            f.close()
            context.bot.sendMessage(chat_id= chat_id, text= "file scritto correttamente")
        else:
            context.bot.sendMessage(chat_id= chat_id, text= "testo non valido o troppo corto")

def readReports(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        f = open("./data/reports.txt", "r")
        tx = f.read()
        f.close()
        if len(tx) < 1:
            tx = "Non ci sono report! Seems we have done a good job 😏"
        context.bot.sendMessage(chat_id= chat_id, text= tx)

def report(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    tx = "\nDa: @" + update.message.from_user.username + "\nMessaggio: " + text[8:] + "\n#report #bugs #bugs #errori\n"
    if len(text) > 10 and text.find(' ') != -1:
        f = open("./data/reports.txt", "a")
        f.write(tx)
        f.close()
        context.bot.sendMessage(chat_id= chat_id, text= phrases["succReport"])
        for el in config_get["autorizzati"]:
            context.bot.sendMessage(chat_id= el, text= tx)
    else:
        context.bot.sendMessage(chat_id= chat_id, text= phrases["errReport"])

def send_report(update, context):
    return ConversationHandler.END

def start_bot(update, context):    
    st = phrases["start"]
    update.message.reply_text(st, reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
