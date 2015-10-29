from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
# http://newcoder.io/scrape/part-3/
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

# ---------------------------
# models.py
# Copyright (C) 2015
# 4Play
# ---------------------------

Base = declarative_base()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''  # insert URI
db = SQLAlchemy(app)


class GamesPlatforms(Base):
    __tablename__ = 'GamesPlatforms'
    game_id = Column(Integer, ForeignKey('Games.id'))
    platform_id = Column(Integer, ForeignKey('Platforms.id'))


class GamesCompanies(Base):
    __tablename__ = 'GamesCompanies'
    game_id = Column(Integer, ForeignKey('Games.id'))
    company_id = Column(Integer, ForeignKey('Companies.id'))
    relation = Column(String)


# ------------
# Game
# ------------
class Games(Base):
    """
    Data model for games, there are 2 dependencies on companies and 1 on platform
    """
    __tablename__ = 'Games'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(String)
    release_date = Column(Date)
    deck = Column(String)
    genres = Column(String)
    franchises = Column(String)
    description = Column(String)

    platforms = relationship("Platforms", secondary=GamesPlatforms,
                             primaryjoin=(GamesPlatforms.game_id == id), backref="games")
    developers = relationship("Companies", secondary=GamesCompanies,
                              primaryjoin=(GamesCompanies.game_id == id and
                                           GamesCompanies.relation == 'developer'), backref="developed_games")
    publishers = relationship("Companies", secondary=GamesCompanies,
                              primaryjoin=(GamesCompanies.game_id == id and
                                           GamesCompanies.relation == 'publishers'), backref="published_games")

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
class Companies(Base):
    """
    Company data model, has 2 dependencies on a Game, one on platform
    """
    __tablename__ = 'Companies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    founded_date = Column(Date)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    state = Column(String)
    deck = Column(String)
    concepts = Column(String)
    phone = Column(String)
    website = Column(String)
    description = Column(String)

    developed_games = relationship("Companies", secondary=GamesCompanies,
                                   primaryjoin=(GamesCompanies.company_id == id and
                                                GamesCompanies.relation == 'developer'), backref="developers")
    published_games = relationship("Companies", secondary=GamesCompanies,
                                   primaryjoin=(GamesCompanies.company_id == id and
                                                GamesCompanies.relation == 'publishers'), backref="publishers")

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        constructor, saves values into model object
        return array args are optional for constructor
        """
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
class Platforms(Base):
    """
    platform data model, has 1 dependency on Game model and 1 on Platform
    """
    __tablename__ = 'Platforms'
    name = Column(String)
    release_date = Column(Date)
    online_support = Column(Boolean)
    price = Column(Float)
    company = Column(String)
    deck = Column(String)
    install_base = Column(Integer)
    description = Column(String)

    # companies = db.relationship('Company', backref=db.backref('platform', lazy='dynamic')
    games = relationship("Games", secondary=GamesPlatforms,
                         primaryjoin=(GamesPlatforms.platform_id == id), backref="platforms")

    # ------------
    # __init__
    # ------------
    def __init__(self, **args):
        """
        array args are optional
        """
        self.name = args.get("name")
        self.release_date = args.get("release_date")
        self.online_support = args.get("online_support", False)
        self.price = args.get("price")
        self.company = args.get("company")
        self.deck = args.get("deck")
        self.install_base = args.get("install_base")
        self.description = args.get("description")
