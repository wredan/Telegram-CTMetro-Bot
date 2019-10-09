from functions import *
import json

with open('./jsonFiles/config.json', 'r') as f:
    config_get = json.load(f)

def main():
    updater = Updater(token=config_get["token"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',startBot))
    dp.add_handler(CommandHandler('help',getHelp))
    dp.add_handler(CommandHandler('info',getInfo))
    dp.add_handler(CommandHandler('metro',getStationsChoice))
    dp.add_handler(CommandHandler('stazioni',getStazioni))
    dp.add_handler(CommandHandler('autori',getAuthor))
    dp.add_handler(CommandHandler('donate',donate))
    dp.add_handler(CommandHandler('report',report))
    dp.add_handler(CommandHandler('chatid',getChatId))
    dp.add_handler(CommandHandler('readReports',readReports))
    dp.add_handler(CommandHandler('clearReports',clearReports))
    dp.add_handler(CommandHandler('listaComandi',getCommandsList))
    dp.add_handler(CallbackQueryHandler(callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()