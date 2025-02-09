import disnake
from disnake.ext import commands

from config import bot, nats_discord_channel_id
from nats_server.handlers import connect_to_nats_handler


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Отвечает «Pong!» и выводит задержку бота")
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(content=f"Pong! `{round(bot.latency * 1000)}ms`")

    @commands.slash_command(name="set_status", description="Устанавливает активность бота")
    async def set_status(
            self,
            inter: disnake.ApplicationCommandInteraction,
            status: str = commands.Param(name="status")
    ):
        activity = disnake.Activity(name=status)
        await bot.change_presence(activity=activity)

        await inter.send(content=f"Активность установлена!", ephemeral=True)

    @commands.slash_command(name="broadcast", description="Публикует указанное сообщение в NATS")
    async def broadcast(
            self,
            inter: disnake.ApplicationCommandInteraction,
            message: str = commands.Param(name="message")
    ):
        await inter.response.defer(ephemeral=True)
        nc = await connect_to_nats_handler()
        await nc.publish(f"broadcast.{nats_discord_channel_id}", bytes(message, encoding="utf8"))

        embed = disnake.Embed(
            description=f"**Сообщение было опубликованно в NATS** ```{message}```",
            color=disnake.Color.dark_embed()
        )

        await inter.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(BotCommands(bot))
