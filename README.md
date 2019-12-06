# Telegram-CTMetrobot-Bot
CTmetrobot lets you know the estimated time of the Catania's next coming underground train in a station or you can use it to find a specific underground train by typing hh:mm time. Let's find out here:
* [@ct_metrobot](http://telegram.me/ct_metrobot)
---

### Setting up a local istance
If you want to test the bot by creating your personal istance, follow this steps:
* **Clone this repository** or download it as zip.
* **Send a message to your bot** on Telegram, even '/start' will do. If you don't, you could get an error
* Copy the file config/settings.json.dist into config/settings.json (If you don't have a token, message Telegram's [@BotFather](http://telegram.me/Botfather) to create a bot and get a token for it)
* Copy the file jsonFiles/metroTimetables.json.dist into jsonFiles/metroTimetables.json
* Copy the file jsonFiles/phrases.json.dist into jsonFiles/phrases.json
* Fill this new files with your data
* Now you can launch "main.py" with your Python3 interpreter

### System requirements

- Python 3
- python-pip3

#### To install with *pip3*

- pip3 install -r requirements.txt

### License
This open-source software is published under the GNU General Public License (GNU GPL) version 3. Please refer to the "LICENSE" file of this project for the full text.