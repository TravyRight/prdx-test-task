import time

from typing import Optional
from sqlalchemy import BIGINT, TIMESTAMP, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class bot_users(Base):
    __tablename__ = "bot_users"

    id: Mapped[int] = mapped_column(Integer, autoincrement="auto", primary_key=True)
    discord_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    joined_at: Mapped[int] = mapped_column(TIMESTAMP, default=time.time())

    def __repr__(self):
        return f"bot_users(id={self.id!r}, discord_id={self.discord_id!r}, username={self.username!r}, username={self.joined_at!r})"
