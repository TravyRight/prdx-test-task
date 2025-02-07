import disnake
from disnake.ext import commands

import sqlite3
import logging
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

intents = disnake.Intents.all()
intents.presences = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=".", intents=intents)

conn = sqlite3.connect("Discord-bot-Rooms/database/database.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s"
)
