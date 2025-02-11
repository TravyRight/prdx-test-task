import asyncio
import logging

from nats.aio.client import Client
from nats.aio.errors import ErrTimeout, ErrNoServers

from config import bot


async def nats_message_handler(msg):
    channel_id = str(msg.subject).split(".")[1]
    channel = await bot.fetch_channel(channel_id)

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

        except (ErrTimeout, ErrNoServers) as e:
            attempts += 1
            logging.error(f"Error connecting to NATS: {e}. Retry after {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)

    logging.critical("Can not connect to NATS!")
    return None
