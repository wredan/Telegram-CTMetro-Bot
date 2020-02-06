# -*- coding: utf-8 -*-

import json
import os
import sys
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from Functions import *
from Settings import *

def main():
    updater = Updater(token=config_get["token"], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('metro',new_metro))
    dp.add_handler(CommandHandler('start',start_bot))
    dp.add_handler(CommandHandler('chatid',get_chat_id))
    dp.add_handler(CommandHandler('dona',donate))

    dp.add_handler(MessageHandler(Filters.regex('Aiuto'), get_help))
    dp.add_handler(MessageHandler(Filters.regex('ℹ️ Info'), get_info))
    dp.add_handler(MessageHandler(Filters.regex('🚉 Stazioni'), get_stazioni))
    dp.add_handler(MessageHandler(Filters.regex('👨‍💻 Chi siamo'), get_author))
    dp.add_handler(MessageHandler(Filters.regex('📜 Lista comandi'),get_lista_comandi))

    dp.add_handler(MessageHandler(Filters.regex('📜 Leggi report'), read_reports))
    dp.add_handler(MessageHandler(Filters.regex('❌ Elimina report'), clear_reports))
    dp.add_handler(MessageHandler(Filters.regex('🔙 Back'), back))
    
    dp.add_handler(CallbackQueryHandler(callback))

    metro = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('🚇 Metro'), get_stazione)],
        states={
            STAZIONE: [MessageHandler(Filters.text, get_orario)],
            ORARIO: [MessageHandler(Filters.regex('^(Adesso|Scegli orario)$'), get_next_metro)],            
            SCEGLIORARIO: [MessageHandler(Filters.text, scegli_orario)]        
        },
        fallbacks=[CommandHandler('annulla', cancel)]
    )

    client_report = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('📢 Report'), report)],
        states={
            SENDMESSAGE: [MessageHandler(Filters.text, send_report)],                      
        },
        fallbacks=[CommandHandler('annulla', cancel)]
    )

    admin_report = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('✏️ Scrivi file report'), report_message)],
        states={
            WRITEMESSAGE: [MessageHandler(Filters.text, write_report)],                      
        },
        fallbacks=[CommandHandler('annulla', abort_report)]
    )
    
    dp.add_handler(metro)
    dp.add_handler(client_report)
    dp.add_handler(admin_report)

    dp.add_error_handler(error)

    def shutdown():
        updater.stop()
        updater.is_idle = False

    def shut_down_bot(update, context):
        chat_id = update.message.chat_id
        text = update.message.text
        if str(chat_id) in config_get["autorizzati"] :
            if text == "/shutdownbot " + str(chat_id):
                context.bot.sendMessage(chat_id= chat_id, text= 'Spengo il bot... arrivederci!')
                Thread(target=shutdown).start()
            else:
                context.bot.sendMessage(chat_id= chat_id, text= 'Il comando corretto è /shutdownbot <chat_id_autorizzato>, usa /chatid per conoscere il tuo chatid')

    dp.add_handler(CommandHandler('shutdownbot',shut_down_bot))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()