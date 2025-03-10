from aiogram.types import Message
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Any

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, index=True, unique=True, primary_key=True)
    username = Column(String(255))
    api_hash = Column(String(255))
    api_id = Column(String(255))

    channel = relationship("Channel", back_populates="owner")

    def __repr__(self) -> str:
        return f"Users(tg_id={self.id}, username={self.username})"

    def to_dict(self) -> dict[str, Column[str] | Column[int]]:
        return {
            'tg_id': self.id,
            'username': self.username,
            'channels': self.channel
        }

    def info(self) -> str:
        return f"Ваш айди: {self.id}\n" \
               f"Ваш ник: {self.username}\n" \
               f"Список ваших каналов: {self.from_channels()}" \

    def from_channels(self) -> list:
        return [channel.name for channel in self.channel]

    @classmethod
    def from_message(cls, message: Message):
        return cls(
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )

class Channel(Base):
    __tablename__ = 'сhannel'

    channel_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("Users", back_populates="channel")

    def __repr__(self) -> str:
        return f"Channel(channel_id={self.channel_id}, user_id={self.user_id})"

    def to_dict(self) -> dict[str, Column[Any]]:
        return {
            'channel_id': self.channel_id,
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
