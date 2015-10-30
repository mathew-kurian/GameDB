#!/usr/bin/env python3

import decimal
import json, datetime
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

# ---------------------------
# models.py
# Copyright (C) 2015
# 4Play
# ---------------------------

Base = declarative_base()


class Serializer(object):
    __public__ = None

    def to_serializable_dict(self):
        dict = {}
        for public_key in self.__public__:
            value = getattr(self, public_key)
            if value:
                dict[public_key] = value
        return dict


class SWEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Serializer):
            return obj.to_serializable_dict()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def to_json(arg, **kwargs):
    kwargs['cls'] = SWEncoder
    return json.dumps(arg, **kwargs)


class GamePlatform(Base, Serializer):
    __tablename__ = 'game_platforms'
    __public__ = ['game_id', 'platform_id', 'platform_name', 'game_name']

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        constructor, saves values into model object
        list args are optional for constructor
        """
        self.game_id = args.get('game_id')
        self.platform_id = args.get('platform_id')


class GameCompany(Base, Serializer):
    __tablename__ = 'games_companies'
    __public__ = ['game_id', 'company_id', 'game_name', 'company_name']

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    role = Column(String(20))

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        constructor, saves values into model object
        list args are optional for constructor
        """
        self.game_id = args.get('game_id')
        self.company_id = args.get('company_id')
        self.role = args.get('role')


class Url(Base, Serializer):
    __tablename__ = 'urls'
    __public__ = ['source']

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    source = Column(Text)
    entity = Column(String(20))
    type = Column(String(20))

    Index("entity_index", entity_id, entity, type)

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        constructor, saves values into model object
        list args are optional for constructor
        """
        self.entity_id = args.get('entity_id')
        self.source = args.get('source')
        self.entity = args.get('entity')
        self.type = args.get('type')


# ------------
# Game
# ------------
class Game(Base, Serializer):
    """
    Data model for games, there are 2 dependencies on companies and 1 on platform
    """
    __tablename__ = 'games'
    __public__ = ['id', 'name', 'rating', 'release_date', 'deck', 'genres', 'franchises', 'description', 'videos',
                  'images', 'platforms', 'developers', 'publishers']

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    rating = Column(String(100))
    release_date = Column(DateTime)
    deck = Column(Text)
    genres = Column(Text)
    franchises = Column(Text)
    description = Column(Text(4294967295))

    videos = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'video'),
                          foreign_keys=[Url.entity_id], viewonly=True)
    images = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'image'),
                          foreign_keys=[Url.entity_id], viewonly=True)

    platforms = relationship(GamePlatform)
    developers = relationship(GameCompany,
                              primaryjoin=and_(GameCompany.game_id == id, GameCompany.role == 'developer'))
    publishers = relationship(GameCompany,
                              primaryjoin=and_(GameCompany.game_id == id, GameCompany.role == 'publisher'))

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        constructor, saves values into model object
        list args are optional for constructor
        """
        self.id = args.get('id')
        self.name = args.get('name')
        self.rating = args.get('rating')
        self.release_date = args.get('release_date')
        self.deck = args.get('deck')
        self.genres = args.get('genres')
        self.franchises = args.get('franchises')
        self.description = args.get('description')


# ------------
# Company
# ------------
class Company(Base, Serializer):
    """
    Company data model, has 2 dependencies on a Game, one on platform
    """
    __tablename__ = 'companies'
    __public__ = ['id', 'name', 'founded_date', 'address', 'city', 'country', 'state', 'deck', 'concepts',
                  'phone', 'website', 'description', 'videos', 'images', 'developed_games', 'published_games',
                  'platforms']

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    founded_date = Column(DateTime)
    address = Column(String(100))
    city = Column(String(100))
    country = Column(String(100))
    state = Column(String(100))
    deck = Column(Text)
    concepts = Column(Text)
    phone = Column(String(100))
    website = Column(String(100))
    description = Column(Text(4294967295))

    videos = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'video'),
                          foreign_keys=[Url.entity_id], viewonly=True)
    images = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'image'),
                          foreign_keys=[Url.entity_id], viewonly=True)

    developed_games = relationship(GameCompany,
                                   primaryjoin=and_(GameCompany.company_id == id, GameCompany.role == 'developer'))
    published_games = relationship(GameCompany,
                                   primaryjoin=and_(GameCompany.company_id == id, GameCompany.role == 'publisher'))

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        constructor, saves values into model object
        return array args are optional for constructor
        """
        self.id = args.get("id")
        self.name = args.get("name")
        self.founded_date = args.get("founded_date")
        self.address = args.get("address")
        self.city = args.get("city")
        self.country = args.get("country")
        self.state = args.get("state")
        self.deck = args.get("deck")
        self.concepts = args.get("concepts")
        self.phone = args.get("phone")
        self.website = args.get("website")
        self.description = args.get("description")


# ------------
# Platform
# ------------
class Platform(Base, Serializer):
    """
    platform data model, has 1 dependency on Game model and 1 on Platform
    """
    __tablename__ = 'platforms'
    __public__ = ['id', 'name', 'release_date', 'online_support', 'price', 'company', 'deck', 'install_base',
                  'description', 'videos', 'images', 'games', 'companies']

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    release_date = Column(DateTime)
    online_support = Column(Boolean)
    price = Column(Float)
    company = Column(String(100))
    deck = Column(Text)
    install_base = Column(Integer)
    description = Column(Text(4294967295))

    videos = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'video'),
                          foreign_keys=[Url.entity_id], viewonly=True)
    images = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'image'),
                          foreign_keys=[Url.entity_id], viewonly=True)

    games = relationship(GamePlatform)

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        array args are optional
        """
        self.id = args.get("id")
        self.name = args.get("name")
        self.release_date = args.get("release_date")
        self.online_support = args.get("online_support", False)
        self.price = args.get("price")
        self.company = args.get("company")
        self.deck = args.get("deck")
        self.install_base = args.get("install_base")
        self.description = args.get("description")


# materialized columns

GameCompany.game_name = column_property(
    select([Game.name]).where(Game.id == GameCompany.game_id)
)

GameCompany.company_name = column_property(
    select([Company.name]).where(Company.id == GameCompany.company_id)
)

GamePlatform.game_name = column_property(
    select([Game.name]).where(Game.id == GamePlatform.game_id)
)

GamePlatform.platform_name = column_property(
    select([Platform.name]).where(Platform.id == GamePlatform.platform_id)
)


# views

class CompanyPlatform(Base, Serializer):
    __public__ = ['company_id', 'platform_id', 'platform_name', 'company_name']
    __mapper_args__ = {
        'primary_key': [GameCompany.company_id, GamePlatform.platform_id]}
    __table__ = select(
        [GameCompany.company_id, GamePlatform.platform_id, GamePlatform.platform_name.label('platform_name'),
         GameCompany.company_name.label('company_name')]). \
        select_from(
        join(GameCompany, GamePlatform,
             GameCompany.game_id == GamePlatform.game_id)
    ).distinct().group_by('company_id', 'platform_id').alias()


# dependent relations

Platform.companies = relationship(CompanyPlatform, primaryjoin=and_(CompanyPlatform.platform_id == Platform.id),
                                  viewonly=True)

Company.platforms = relationship(CompanyPlatform, primaryjoin=and_(CompanyPlatform.company_id == Company.id),
                                 viewonly=True)
