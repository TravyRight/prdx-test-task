import datetime
import time

import disnake
from disnake.ext import commands
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import bot, nats_discord_channel_id, engine
from database.models import bot_users
from nats_server.handlers import connect_to_nats_handler


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_slash_command_check(self, inter: disnake.ApplicationCommandInteraction):
        with Session(engine) as session:
            query = session.query(bot_users).filter(bot_users.discord_id == inter.user.id).first()

            if query is None and inter.application_command.name != "register":
                await inter.send(content="Вы не зарегистрированы! Используйте `/register`")
                return False

        return True

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

        with Session(engine) as session:
            query = session.query(bot_users).filter(bot_users.discord_id == inter.user.id).first()

            if query is not None:
                await inter.send(content="Упс... Вы уже зарегистрированы", ephemeral=True)
                return

            new_bot_user = bot_users(
                discord_id=inter.user.id,
                username=inter.user.name,
                joined_at=round(inter.user.joined_at.timestamp())
            )

            session.add(new_bot_user)
            session.commit()

        await inter.send(content="Вы были **успешно** зарегистрированы", ephemeral=True)

    @commands.slash_command(name="user_info", description="Информация о пользователе")
    async def user_info(
            self,
            inter: disnake.ApplicationCommandInteraction,
            user: disnake.Member = commands.Param(name="user", default=None)
    ):
        await inter.response.defer(ephemeral=True)

        if user is None:
            user = inter.user

        with Session(engine) as session:
            data = select(bot_users).where(bot_users.discord_id == user.id)

            try:
                user = session.scalars(data).one()
            except:
                await inter.send(content="Упс... Пользователя нет в базе", ephemeral=True)
                return

        embed = disnake.Embed(
            title="Информация",
            color=disnake.Color.dark_embed()
        )

        embed.add_field(
            name="1. `discord_id`",
            value=str(user.discord_id),
            inline=False
        )

        embed.add_field(
            name="2. `username`",
            value=user.username,
            inline=False
        )

        embed.add_field(
            name="3. `joined_at`",
            value=f"<t:{user.joined_at}:R>",
            inline=False
        )

        await inter.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(BotCommands(bot))
