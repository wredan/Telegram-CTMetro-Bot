# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from supportFunctions import *
import json

with open('./jsonFiles/metroTimetables.json', 'r') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r') as f:
    phrases = json.load(f)

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

# def getMetro(bot, update):
#     mex = update.message.text
#     chat_id = update.message.chat_id
#     if checkTime(bot, chat_id):
#         timeNes = getMetroTime(mex[7:], "NESIMA", "STESICORO")
#         timeSte = getMetroTime(mex[7:], "STESICORO", "NESIMA")
#         time = timeNes+"\n"+timeSte
#         bot.send_message(chat_id=chat_id, text= time)    

def callback(bot, update):
    query = update.callback_query
    if checkTime(bot, query):
        timeNes = getMetroTime(query.data, "NESIMA", "STESICORO", datetime.now())
        timeSte = getMetroTime(query.data, "STESICORO", "NESIMA", datetime.now())
        time = timeNes+"\n"+timeSte
        query.edit_message_text(text= time)

def getInfo(bot, update):
    info = phrases["info"]
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text= info) 

def getChatId(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= chat_id)
    
def getAuthor(bot, update):
    aut = phrases["author"]
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= aut)

def startBot(bot, update):
    st = phrases["start"]
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= st)

def getStazioni(bot, update):
    mex = ""
    for el in metroTime["STAZIONI"]:
        mex+=el+"\n"
    chat_id = update.message.chat_id
    bot.send_message(chat_id= chat_id, text= mex)
