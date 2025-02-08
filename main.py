import logging

from config import TOKEN, bot


def main():
    logging.info("Start bot")

    """
    logging.info("Create db")
    create_db()
    """

    logging.info("Load cogs")
    bot.load_extension("cogs.commands")

    @bot.event
    async def on_ready():
        on_ready_message = "Bot is ready"
        logging.info(on_ready_message)
        print(on_ready_message)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
