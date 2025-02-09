import logging

from nats.errors import BadSubjectError

from config import TOKEN, bot
from nats_server.handlers import nats_message_handler, connect_to_nats_handler


def main():
    logging.info("Start bot")

    """
    logging.info("Create db")
    create_db()
    """

    logging.info("Load cogs")
    bot.load_extension("cogs.commands")
    # bot.load_extension("cogs.tasks")

    @bot.event
    async def on_ready():
        log_message = "Bot is ready"
        logging.info(log_message)
        print(log_message)

        # connect and subscribe to NATS
        nc = await connect_to_nats_handler()
        await nc.subscribe("broadcast.*", cb=nats_message_handler)


    @bot.event
    async def on_disconnect():
        await nc.close()

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
