#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Text,
    ForeignKey,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text(), unique=True, nullable=False)
    chat_id = Column(Text(), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

class LunchMenu(Base):
    __tablename__ = 'lunchmenus'
    id = Column(Integer, primary_key=True)
    description = Column(Text(), nullable=False)
    date = Column(Date(), nullable=False)

class LunchRating(Base):
    __tablename__ = 'lunchratings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),
        nullable=False)
    lunchmenu_id = Column(Integer, ForeignKey('lunchmenus.id'),
        nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    lunchmenu = relationship("LunchMenu", back_populates="ratings")

User.ratings = relationship('LunchRating', back_populates="user")
LunchMenu.ratings = relationship("LunchRating", back_populates="lunchmenu")