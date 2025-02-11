import asyncio
import logging

from nats.aio.client import Client
from nats.aio.errors import ErrTimeout, ErrNoServers

from config import bot


async def nats_message_handler(msg):
    channel_id = str(msg.subject).split(".")[1]
    channel = await bot.fetch_channel(int(channel_id))

    """
    Изначально строка 12 выглядела так:
    channel = await bot.fetch_channel(channel_id)
    
    Удивительно, но этот код работал.
    Я посмотрел код метода fetch_message и оказалось, 
    что для получения канала можно передать channel_id
    не только c типом int, но и с типом str. 
    
    Лучше добавить int() на случай, если разработчики disnake что-либо поменяют
    """

    if channel is not None:
        await channel.send(content=msg.data.decode())


async def connect_to_nats_handler(max_retries=5, retry_delay=2):
    nc = Client()
    attempts = 0

    while attempts < max_retries:
        try:
            await nc.connect(servers=["nats://localhost:4222"])
            logging.info("Successful connection to NATS!")
            return nc

        except Exception as e:  # (ErrTimeout, ErrNoServers)
            attempts += 1
            logging.error(f"Error connecting to NATS: {e}. Retry after {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)

    logging.critical("Can not connect to NATS!")
    return None
