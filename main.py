import disnake
from disnake.ext import commands

import logging

from config import TOKEN, bot


def main():
    logging.info("Start bot")

    logging.info("Load cogs")
    bot.load_extension("cogs.commands")

    @bot.event
    async def on_ready():
        print("bot is ready")

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
