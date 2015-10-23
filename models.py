from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
# http://newcoder.io/scrape/part-3/
from sqlalchemy import Table, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable

make_searchable()

# ---------------------------
# models.py
# Copyright (C) 2015
# 4Play
# ---------------------------

Base = declarative_base()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''  # insert URI
db = SQLAlchemy(app)


class Game_Company_table(db.Model):
    __tablename__ = 'game-company association'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, ForeignKey('game.id'))
    company_id = db.Column(db.Integer, ForeignKey('company.id'))


class Game_Platform_table(db.Model):
    __tablename__ = 'game-platform association'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, ForeignKey('game.id'))
    platform_id = db.Column(db.Integer, ForeignKey('platform.id'))


# ------------
# Game
# ------------

class Game(db.Model):
    """
    Data model for games, there are 2 dependencies on companies and 1 on platform
    """
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)  # insert number into db.String()
    release_date = db.Column(db.String(), unique=True)
    genres = db.Column(db.PickleType(), unique=True)
    description = db.Column(db.String(), unique=True)
    deck = db.Column(db.String(), unique=True)
    videos = db.Column(db.PickleType(), unique=True)
    images = db.Column(db.PickleType(), unique=True)

    platforms = relationship('Platform', secondary=Game_Platform_table, backref=db.backref('game', lazy='dynamic'))
    developers = relationship('Company', secondary=Game_Company_table, backref=db.backref('game', lazy='dynamic'))
    publishers = relationship('Company', secondary=Game_Company_table, backref=db.backref('game', lazy='dynamic'))

    # ------------
    # __init__
    # ------------
    def __init__(self, name, release_date, description, deck, **args):
        """
        constructor, saves values into model object
        list args are optional for constructor
        """
        self.name = name
        self.release_date = release_date
        self.genres = args.get("genres", None)
        self.description = description
        self.deck = deck
        self.videos = args.get("videos", None)
        self.images = args.get("images", None)
        self.developers = args.get("developers", None)
        self.publishers = args.get("publishers", None)
        self.platforms = args.get("platforms", None)

    # ------------
    # __repr__
    # ------------
    def __repr__(self):
        """
        return name
        """
        return '<Game %r>' % self.name


# ------------
# Company
# ------------
class Company(db.Model):
    """
    Company data model, has 2 dependencies on a Game, one on platform
    """
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    location_address = db.Column(db.String(), unique=True)
    location_city = db.Column(db.String(), unique=True)
    location_state = db.Column(db.String(), unique=True)
    location_country = db.Column(db.String(), unique=True)
    phone = db.Column(db.String(), unique=True)
    images = db.Column(db.PickleType, unique=True)
    website = db.Column(db.String(), unique=True)
    description = db.Column(db.String(), unique=True)

    platforms = db.relationship('Platform', backref=db.backref('game', lazy='dynamic'))
    developed_games = relationship('Game', secondary=Game_Company_table, backref=db.backref('company', lazy='dynamic'))
    published_games = relationship('Game', secondary=Game_Company_table, backref=db.backref('company', lazy='dynamic'))

    # ------------
    # __init__
    # ------------
    def __init__(self, name, location_address, location_city, location_state, location_country, phone, website,
                 description, **args):
        """
        constructor, saves values into model object
        return array args are optional for constructor
        """
        self.name = name
        self.location_address = location_address
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country
        self.phone = phone
        self.images = args.get("images", None)
        self.website = website
        self.description = description
        self.platforms = args.get("platforms", None)
        self.developed_games = args.get("developed_games", None)
        self.published_games = args.get("published_games", None)

    # ------------
    # __repr__
    # ------------
    def __repr__(self):
        """
        return name
        """
        return '<Developer %r>' % self.name


# ------------
# Platform
# ------------
class Platform(db.Model):
    """
    platform data model, has 1 dependency on Game model and 1 on Platform
    """
    __tablename__ = 'platform'
    id = db.Column(db.Integer, primary_key=True)
    release_date = db.Column(db.String(), unique=True)
    price = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String(), unique=True)
    online_support = db.Column(db.Boolean(), unique=True)
    description = db.Column(db.String(), unique=True)
    deck = db.Column(db.String(), unique=True)
    images = db.Column(db.PickleType(), unique=True)

    companies = db.relationship('Company',
                                backref=db.backref('platform', lazy='dynamic'))
    games = relationship('Game', backref=db.backref('platform', lazy='dynamic'))

    # ------------
    # __init__
    # ------------
    def __init__(self, release_date, name, price, online_support, description, deck, **args):
        """
        array args are optional
        """
        self.release_date = release_date
        self.name = name
        self.price = price
        self.online_support = online_support
        self.description = description
        self.deck = deck
        self.images = args.get("images", None)
        self.companies = args.get("companies", None)
        self.games = args.get("games", None)

    # ------------
    # __repr__
    # ------------
    def __repr__(self):
        """
        return name
        """
        return '<Platform %r>' % self.name
