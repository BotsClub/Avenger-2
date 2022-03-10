import json
import sys
from random import randint
from time import time

import aiohttp
from Avenger import aiohttpsession
from aiohttp import ClientSession

from google_trans_new import google_translator
from Python_ARQ import ARQ
from search_engine_parser import GoogleSearch

from Avenger import BOT_ID, OWNER_ID, ARQ_API_URL, ARQ_API_KEY
from Avenger import pbot

ARQ_API = "RKPQLU-TXPMHP-VODILW-OMJSVR-ARQ"
ARQ_API_KEY = "RKPQLU-TXPMHP-VODILW-OMJSVR-ARQ"
SUDOERS = OWNER_ID
ARQ_API_URL = "https://thearq.tech"

print("[AVENGER]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
print("[AVENGER]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

app = pbot
import socket
