from functions import *
import json

with open('./jsonFiles/config.json', 'r') as f:
    config_get = json.load(f)

def main():
    updater = Updater(token=config_get["token"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',startBot))
    dp.add_handler(CommandHandler('metro',getMetro))
    dp.add_handler(CommandHandler('info',getInfo))
    dp.add_handler(CommandHandler('autori',getAuthor))
    dp.add_handler(CommandHandler('stazioni',getStazioni))
    dp.add_handler(CommandHandler('chatid',getChatId))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()