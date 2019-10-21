# -*- coding: utf-8 -*-
from functions import *
import json
import os
import sys
from threading import Thread

with open('./jsonFiles/config.json', 'r') as f:
    config_get = json.load(f)

def main():
    updater = Updater(token=config_get["token"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',startBot))
    dp.add_handler(CommandHandler('aiuto',getHelp))
    dp.add_handler(CommandHandler('info',getInfo))
    dp.add_handler(CommandHandler('metro',getMetro))
    dp.add_handler(CommandHandler('stazioni',getStazioni))
    dp.add_handler(CommandHandler('chisiamo',getAuthor))
    dp.add_handler(CommandHandler('dona',donate))
    dp.add_handler(CommandHandler('report',report))
    dp.add_handler(CommandHandler('chatid',getChatId))
    dp.add_handler(CommandHandler('readReports',readReports))
    dp.add_handler(CommandHandler('clearReports',clearReports))
    dp.add_handler(CommandHandler('writeReports',writeOnReportsFile))
    dp.add_handler(CommandHandler('listaComandi',getCommandsList))

    dp.add_handler(CallbackQueryHandler(callback))

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