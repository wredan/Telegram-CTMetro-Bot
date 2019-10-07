from functions import *
import json

with open('config.json', 'r') as f:
    config_get = json.load(f)

def main():
    updater = Updater(token=config_get["token"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('metro',getMetro))
    dp.add_handler(CommandHandler('info',getInfo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()