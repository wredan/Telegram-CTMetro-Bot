# -*- coding: utf-8 -*-

from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from supportFunctions import *
import json
import time

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r') as f:
    phrases = json.load(f)

with open('./jsonFiles/config.json', 'r') as f:
    config_get = json.load(f)

sleepTime = 0.200

def callback(bot, update):
    query = update.callback_query
    if str(query.data) == "clearReportFile":
        f = open("reports.txt", "w")
        f.write('')
        f.close()
        query.edit_message_text(text= "File ripulito correttamente")
    elif str(query.data) == "none":
        query.edit_message_text(text= "Operazione annullata")
    elif checkTime(bot, query):
        time = getTime(query.data)
        query.edit_message_text(text= time)

def clearReports(bot, update):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        keyboard = [[InlineKeyboardButton("Si", callback_data='clearReportFile'), InlineKeyboardButton("No", callback_data='none')]]
        update.message.reply_text('Sicuro di voler eliminare tutti i report?', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        time.sleep(sleepTime)
        tx = "Ciao " + update.message.from_user.first_name + phrases["readReports"]
        bot.send_message(chat_id= chat_id, text= tx)

def donate(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id= chat_id, text= phrases["donate"])

def getAuthor(bot, update):
    aut = phrases["author"]
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(sleepTime)
    bot.send_message(chat_id= chat_id, text= aut)

def getChatId(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= chat_id)

def getCommandsList(bot, update):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        bot.send_message(chat_id= chat_id, text= config_get["commandsList"])
    else:
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        time.sleep(sleepTime)
        getHelp(bot, update)

def getHelp(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(sleepTime)
    bot.send_message(chat_id= chat_id, text= phrases["help"])

def getInfo(bot, update):
    info = phrases["info"]
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(sleepTime)
    bot.send_message(chat_id=chat_id, text= info) 

def getMetro(bot, update):
    tx = update.message.text
    if len(tx) < 7:
        getStationsChoice(bot, update)
    elif checkTime(bot, update, sel= 1, chat_id= update.message.chat_id) and checkInput(tx[7:]):
        times = tx.split(':')
        time = timedelta(hours= times[1], minutes= times[2])
        t = getTime(time)
        bot.send_message(chat_id= update.message.chat_id, text= t)

def getStationsChoice(bot, update):
    # if len(update.message.text)>6:
    #     getMetro()  
    keyboard = [[InlineKeyboardButton("NESIMA", callback_data='NESIMA'),
                InlineKeyboardButton("SAN NULLO", callback_data='SAN NULLO'),
                InlineKeyboardButton("MILO", callback_data='MILO')],
                [InlineKeyboardButton("BORGO", callback_data='BORGO'),
                InlineKeyboardButton("GIUFFRIDA", callback_data='GIUFFRIDA'),
                InlineKeyboardButton("ITALIA", callback_data='ITALIA')],
                [InlineKeyboardButton("GALATEA", callback_data='GALATEA'),
                InlineKeyboardButton("GIOVANNI XXIII", callback_data='GIOVANNI XXIII'),
                InlineKeyboardButton("STESICORO", callback_data='STESICORO')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Scegli una stazione (sono ordinate da NESIMA a STESICORO):', reply_markup=reply_markup)
    
def getStazioni(bot, update):
    mex = ""
    for el in metroTime["STAZIONI"]:
        mex+=el+"\n"
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(sleepTime)
    bot.send_message(chat_id= chat_id, text= mex)

def writeOnReportsFile(bot, update):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        tx = update.message.text
        if len(tx) > 14:
            f = open("reports.txt", "w")
            f.write(tx[14:])
            f.close()
            bot.send_message(chat_id= chat_id, text= "file scritto correttamente")
        else:
            bot.send_message(chat_id= chat_id, text= "testo non valido o troppo corto")
    else:
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        tx = "Ciao " + update.message.from_user.first_name + phrases["readReports"]
        bot.send_message(chat_id= chat_id, text= tx)

def readReports(bot, update):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        f = open("reports.txt", "r")
        tx = f.read()
        f.close()
        if len(tx) < 1:
            tx = "Non ci sono report! Seems we have done a good job 😏"
        bot.send_message(chat_id= chat_id, text= tx)
    else:
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        time.sleep(sleepTime)
        tx = "Ciao " + update.message.from_user.first_name + phrases["readReports"]
        bot.send_message(chat_id= chat_id, text= tx)

def report(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(sleepTime)
    text = update.message.text
    tx = "\nDa: @" + update.message.from_user.username + "\nMessaggio: " + text[8:] + "\n#report #bugs #bugs #errori\n"
    if len(text) > 10 and text.find(' ') != -1:
        f = open("reports.txt", "a")
        f.write(tx)
        f.close()
        bot.send_message(chat_id= chat_id, text= phrases["succReport"])
        for el in config_get["autorizzati"]:
            bot.send_message(chat_id= el, text= tx)
    else:
        bot.send_message(chat_id= chat_id, text= phrases["errReport"])

def startBot(bot, update):
    st = phrases["start"]
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    time.sleep(sleepTime)
    bot.send_message(chat_id= chat_id, text= st)