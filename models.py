from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
#http://newcoder.io/scrape/part-3/
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' #insert URI
db = SQLALchemy(app)

class Game(db.Model):
	__tablename__ = 'games'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True) #insert number into db.String()
	genre = db.Column(db.String(), unique = True)
	
	platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
	platform = db.relationship('Platform', backref = db.backref('games', lazy = 'dynamic'))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
	company = db.relationship('Company', backref = db.backref('games', lazy = 'dynamic'))
	
	engine = db.Column(db.String(), unique = True)
	tags = db.Column(db.String(), unique = True)
	rating = db.Column(db.Integer(), unique = True)
	def __init__(self, genre, platform, publisher, engine, tags, rating):
		self.name = name
		self.genre = genre
		self.platform = platform
		self.company = company
		self.engine = engine
		self.tags = tags
		self.rating = rating
	def __repr__(self):
		return '<Game %r>' % self.name

class Company(db.Model):
	__tablename__ = 'developers'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True)
	location = db.Column(db.String(), unique = True)
	games = db.Column(db.String(), unique = True) #???
	year = db.Column(db.Integer(), unique = True)
	CEO = db.Column(db.String(), unique = True)
	COO = db.Column(db.String(), unique = True)
	employee_count = db.Column(db.Integer(), unique = True)
	def __init__(self, name, location, games, year, CEO, COO, employee_count):
		self.name = name
		self.location = location
		self.games = games
		self.year = year
		self.CEO = CEO
		self.COO = COO
		self.employee_count = employee_coun
	def __repr__(self):
		return '<Developer %r>' % self.name
class Platform(db.Model):
	__tablename__ = 'platforms'
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