# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, ConversationHandler
from Modules.Keyboard import *
from Modules.Metro import *
from Modules.Report import *
from Settings import *

def donate(update, context):
    update.message.reply_text(text= phrases["donate"] + config_get["link_donazione"])

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

def get_stazioni(update, context):
    mex = ""
    for el in metroTime["STAZIONI"]:
        mex+="🚉 "+ el + "\n\n"
    update.message.reply_text(mex)        


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Arrivederci, a presto!',
                              reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))
    return ConversationHandler.END

def start_bot(update, context):    
    st = phrases["start"]
    update.message.reply_text(st, reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))

def new_metro(update, context):
    st = "Ciao! Abbiamo fatto un nuovo aggiornamento che cambia un po' l'esperienza d'uso del bot, speriamo ti piaccia! Per ulteriori chiarimenti, segui i pulsanti in tastiera. Buona esperienza 😄"
    update.message.reply_text(st, reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def back(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) in config_get["autorizzati"]:
        update.message.reply_text('Uff 😥! Vita difficile quella dell\'admin! Ben fatto! 👍🏻', reply_markup=ReplyKeyboardMarkup(get_default_keyboard(), resize_keyboard=True))

def callback(update, context):
    query = update.callback_query
    if str(query.data) == "clear_report_file":
        f = open("./data/reports.txt", "w")
        f.write('')
        f.close()
        query.edit_message_text(text= "File ripulito correttamente")
    elif str(query.data) == "none":
        query.edit_message_text(text= "Operazione annullata")