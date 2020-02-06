# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, ConversationHandler
from Modules.Keyboard import *
from Settings import *
import os
import sys
import logging

SENDMESSAGE = range(1)

WRITEMESSAGE = range(1)

def report_message(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        tx = "Inserisci il testo da scrivere.\nNOTA BENE: verrà sovrascritto tutto il file, quindi copia il contenuto, modificalo e incollalo qui. /annulla per annullare l'azione"
        update.message.reply_text(tx, reply_markup=ReplyKeyboardRemove())
        return  WRITEMESSAGE
    return ConversationHandler.END

def write_report(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        tx = update.message.text
        testo = update.message.text
        f = open("./data/reports.txt", "w")
        f.write(tx)
        f.close()
        update.message.reply_text("File scritto correttamente", reply_markup=ReplyKeyboardMarkup(get_admin_report_keyboard(), resize_keyboard=True))
    return ConversationHandler.END

def read_reports(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        f = open("./data/reports.txt", "r")
        tx = f.read()
        f.close()
        if len(tx) < 1:
            tx = "Non ci sono report! Seems we have done a good job 😏"
        update.message.reply_text(tx)

def report(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        update.message.reply_text('Ecco la tastiera admin, usala bene mi raccomando 👀', reply_markup=ReplyKeyboardMarkup(get_admin_report_keyboard(), resize_keyboard=True))
        return ConversationHandler.END
    else:
        tx = '''Grazie per aver scelto di segnalarci i problemi che hai con il bot. Ti ricordiamo che inviando il messaggio acconsenti implicitamente ad essere ricontattato da uno degli sviluppatori per ulteriori chiarimenti. 
Non ti disturberemo se non sarà strettamente necessario!
Detto ciò inserisci qui il tuo messaggio o digita /annulla per annullare:'''
        update.message.reply_text(tx, reply_markup=ReplyKeyboardRemove())
        return SENDMESSAGE
    
def send_report(update, context):
    text = update.message.text
    tx = "\nDa: @" + update.message.from_user.username + "\nMessaggio: " + text + "\n#report #bugs #bugs #errori\n"
    if len(text) > 10:
        f = open("./data/reports.txt", "a")
        f.write(tx)
        f.close()        
        update.message.reply_text(phrases["succReport"], reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))
        for el in config_get["autorizzati"]:
            context.bot.sendMessage(chat_id= el, text= tx)  
        return ConversationHandler.END     
    else:
        update.message.reply_text(phrases["errReport"])
        return SENDMESSAGE           

def clear_reports(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        keyboard = [[InlineKeyboardButton("Si", callback_data='clear_report_file'), InlineKeyboardButton("No", callback_data='none')]]
        update.message.reply_text('Sicuro di voler eliminare tutti i report?', reply_markup=InlineKeyboardMarkup(keyboard))

def abort_report(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        update.message.reply_text("👍🏻 Azione annullata", reply_markup=ReplyKeyboardMarkup(get_admin_report_keyboard(), resize_keyboard=True))
    return ConversationHandler.END