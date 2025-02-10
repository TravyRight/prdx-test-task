import disnake
from disnake.ext import commands

from config import bot, nats_discord_channel_id
from nats_server.handlers import connect_to_nats_handler


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_slash_command_check(self, inter: disnake.ApplicationCommandInteraction):
        if inter.application_command.name != "register":
            await inter.send(content="Вы не зарегистрированы! Используйте `/register`")
            return

        # check if inter.user in db or not

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

    @commands.slash_command(name="register", description="Регистрация пользователя")
    async def register(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)

        # Добавление inter.user в бд

        await inter.send(content="Вы были **успешно** зарегистрированы", ephemeral=True)

    @commands.slash_command(name="user_info", description="Информация о пользователе")
    async def user_info(
            self,
            inter: disnake.ApplicationCommandInteraction,
            user: disnake.Member = commands.Param(name="message", default=None)
    ):
        await inter.response.defer(ephemeral=True)

        if user is None:
            user = inter.user

        # Достаем инфу об inter.user из бд

        await inter.send(content="В разработке...", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(BotCommands(bot))
