import disnake
from disnake.ext import commands

import logging
import os

from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine
#from database.models import Base


# get token
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

# create discord-bot
intents = disnake.Intents.all()
intents.presences = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=".", intents=intents)

# NATS
nats_discord_channel_id = 1338165876029132930

# create database
#engine = create_engine(url="sqlite:///database/database.db", echo=True)
#Base.metadata.create_all(engine)

# create log file
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s"
)
