from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

# ---------------------------
# models.py
# Copyright (C) 2015
# 4Play
# ---------------------------

Base = declarative_base()


class GamePlatform(Base):
    __tablename__ = 'game_platforms'
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


class GameCompany(Base):
    __tablename__ = 'games_companies'
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


class Url(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer)
    source = Column(Text)
    entity = Column(String(20))
    type = Column(String(20))

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
class Game(Base):
    """
    Data model for games, there are 2 dependencies on companies and 1 on platform
    """
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    rating = Column(String(100))
    release_date = Column(DateTime)
    deck = Column(Text)
    genres = Column(Text)
    franchises = Column(Text)
    description = Column(Text(4294967295))

    videos = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'video'),
                          foreign_keys=Url.entity_id)
    images = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'image'),
                          foreign_keys=Url.entity_id)

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
class Company(Base):
    """
    Company data model, has 2 dependencies on a Game, one on platform
    """
    __tablename__ = 'companies'
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
                          foreign_keys=Url.entity_id)
    images = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'image'),
                          foreign_keys=Url.entity_id)

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
class Platform(Base):
    """
    platform data model, has 1 dependency on Game model and 1 on Platform
    """
    __tablename__ = 'platforms'
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
                          foreign_keys=Url.entity_id)
    images = relationship(Url, primaryjoin=and_(Url.entity_id == id, Url.entity == __tablename__, Url.type == 'image'),
                          foreign_keys=Url.entity_id)

    # companies = db.relationship('Company', backref=db.backref('platform', lazy='dynamic')
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
