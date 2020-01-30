# -*- coding: utf-8 -*-

from functions import *
import json
import os
import sys
from threading import Thread
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, CallbackContext


with open('./config/config.json', 'r', errors='ignore') as f:
    config_get = json.load(f)

def main():
    updater = Updater(token=config_get["token"], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start_bot))
    dp.add_handler(CommandHandler('chatid',get_chat_id))
    dp.add_handler(CommandHandler('readReports',readReports))
    dp.add_handler(CommandHandler('clearReports',clearReports))
    dp.add_handler(CommandHandler('writeReports',writeOnReportsFile))
    dp.add_handler(MessageHandler(Filters.regex('Aiuto'), get_help))
    dp.add_handler(MessageHandler(Filters.regex('ℹ️ Info'), get_info))
    dp.add_handler(MessageHandler(Filters.regex('🚉 Stazioni'), get_stazioni))
    dp.add_handler(MessageHandler(Filters.regex('👨‍💻 Chi siamo'), get_author))
    dp.add_handler(MessageHandler(Filters.regex('💙 Dona'), donate))
    dp.add_handler(MessageHandler(Filters.regex('📜 Lista comandi'),get_lista_comandi))
    dp.add_handler(CallbackQueryHandler(callback))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('🚇 Metro'), get_stazione)],

        states={
            STAZIONE: [MessageHandler(Filters.text, get_orario)],

            ORARIO: [MessageHandler(Filters.regex('^(Adesso|Scegli orario)$'), get_next_metro)],            

            SCEGLIORARIO: [MessageHandler(Filters.text, scegli_orario)]
                      
        },

        fallbacks=[CommandHandler('cancella', cancel)]
    )

    conv_hand = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('📢 Report'), report)],

        states={
            REPMESSAGE: [MessageHandler(Filters.text, send_report)],                      
        },

        fallbacks=[CommandHandler('cancella', cancel)]
    )
    
    dp.add_handler(conv_handler)
    dp.add_handler(conv_hand)

    dp.add_error_handler(error)

    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        chat_id = update.message.chat_id
        text = update.message.text
        if str(chat_id) in config_get["autorizzati"] :
            if text == "/restartbot " + str(chat_id):
                bot.send_message(chat_id= chat_id, text= 'Riavviando il bot...')
                Thread(target=stop_and_restart).start()
            else:
                bot.send_message(chat_id= chat_id, text= 'Il comando corretto è /restartbot <chat_id_autorizzato>, usa /chatid per conoscere il tuo chatid')

    def shutdown():
        updater.stop()
        updater.is_idle = False

    def shutDownBot(bot, update):
        chat_id = update.message.chat_id
        text = update.message.text
        if str(chat_id) in config_get["autorizzati"] :
            if text == "/shutdownbot " + str(chat_id):
                bot.send_message(chat_id= chat_id, text= 'Spengo il bot... arrivederci!')
                Thread(target=shutdown).start()
            else:
                bot.send_message(chat_id= chat_id, text= 'Il comando corretto è /shutdownbot <chat_id_autorizzato>, usa /chatid per conoscere il tuo chatid')

    dp.add_handler(CommandHandler('restartbot',restart))
    dp.add_handler(CommandHandler('shutdownbot',shutDownBot))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()