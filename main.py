import asyncio
import logging

from nats.errors import BadSubjectError

from config import TOKEN, bot
from grpc_server.server import serve
from nats_server.handlers import nats_message_handler, connect_to_nats_handler


def main():
    try:
        logging.info("Start bot")

        """
        logging.info("Create db")
        create_db()
        """

        logging.info("Load cogs")
        bot.load_extension("cogs.commands")

    except Exception as e:
        logging.error(f"Failed to start bot. Error: {str(e)}")
        print(e)

    @bot.event
    async def on_ready():
        log_message = "Bot is ready"
        logging.info(log_message)
        print(log_message)

        # start gRPC server
        grpc_task = asyncio.create_task(serve())

        # connect and subscribe to NATS
        nc = await connect_to_nats_handler()
        await nc.subscribe("broadcast.*", cb=nats_message_handler)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
