import disnake
from disnake.ext import commands

from config import bot


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


def setup(bot: commands.Bot):
    bot.add_cog(BotCommands(bot))
