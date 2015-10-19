from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
#http://newcoder.io/scrape/part-3/
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' #insert URI
db = SQLALchemy(app)

class Game(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True) #insert number into db.String()
	genre = db.Column(db.String(), unique = True)
	
	platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
	platform = db.relationship('Platform', backref = db.backref('games', lazy = 'dynamic'))
	developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'))
	developer = db.relationship('Developer', backref = db.backref('games', lazy = 'dynamic'))
	
	engine = db.Column(db.String(), unique = True)
	tags = db.Column(db.String(), unique = True)
	rating = db.Column(db.Integer(), unique = True)
	def __init__(self, genre, platform, publisher, engine, tags, rating):
		self.name = name
		self.genre = genre
		self.platform = platform
		self.developer = developer
		self.engine = engine
		self.tags = tags
		self.rating = rating
	def __repr__(self):
		return '<Game %r>' % self.name
class Developer(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True)
	location = db.Column(db.String(), unique = True)
	games = db.Column(db.String(), unique = True) #???
	year = db.Column(db.Integer(), unique = True)
	CEO = db.Column(db.String(), unique = True)
	COO = db.Column(db.String(), unique = True)
	employee_count =  = db.Column(db.Integer(), unique = True)
	def __init__(self, name, location, games, year, CEO, COO, employee_count):
		self.name = name
		self.location = location
		self.games = games
		self.year = year
		self.CEO = CEO
		self.COO = COO
		self.employee_count = employee_count
	def __repr__(self):
		return '<Developer %r>' % self.name
class Platform(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	release_date = db.Column(db.String(), unique = True)
	rating = db.Column(db.Integer(), unique = True)
	name = db.Column(db.String(), unique = True)
	num_units = db.Column(db.Integer(), unique = True)
	generation = db.Column(db.String(), unique = True)
	def __init__(self, release_date, rating, name, num_units, generation):
		self.release_date = release_date
		self.rating = rating
		self.name = name
		self.num_units = num_units
		self.generation = generation
	def __repr__(self):
		return '<Platform %r>' % self.name
class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	source = db.Column(db.String(), unique = True)
	entity = db.Column(db.String(), unique = True)
	key = db.Column(db.String(), unique = True)
	type = db.Column(db.String(), unique = True)
	def __init__(self, source, entity, key, type):
		self.source = source
		self.entity = entity
		self.key = key
		self.type = type
	def __repr__(self):
		return '<Image %r>' % self.source