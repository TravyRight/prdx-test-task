import disnake
from disnake.ext import commands

import logging
import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from database.models import Base


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

# create and connect database
# я не стал добавлять информацию об бд в файл .env тк она локальная
user = "postgres"
password = "root"
host = "localhost"
port = 5433
dbname = "prdx_test_task"

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
Base.metadata.create_all(engine)

# create log file
logging.basicConfig(
    level=logging.INFO,
    filename="prdx-test-task/logs.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s"
)
