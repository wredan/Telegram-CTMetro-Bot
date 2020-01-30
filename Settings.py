# -*- coding: utf-8 -*-

import json
import logging

global metroTime
global phrases
global config_get

with open('./jsonFiles/metroTimetables.json', 'r',errors='ignore') as f:
    metroTime = json.load(f)

with open('./jsonFiles/phrases.json', 'r', errors='ignore') as f:
    phrases = json.load(f)

with open('./config/config.json', 'r', errors='ignore') as f:
    config_get = json.load(f)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

global logger 
logger = logging.getLogger(__name__)