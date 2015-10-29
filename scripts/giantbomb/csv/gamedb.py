import models.py
import sqlalchemy

def load_data(file_name):
	data = genfromtxt(file_name, '\n', skiprows=1, converters={0: lambda s: str(s)})
	return data.tolist()
	
Base = declarative_base()

if __name__ == "__main__":
	engine = create_engine("mysql:///games.db")
	Base.metadata.create_all(engine)
	
	session = sessionmaker()
	session.configure(bind=engine)
	s = session()
	
	try:
		file_name = ["games.csv", "companies.csv", "platforms.csv"]
		data1 = load_data(file_name[0])
		for i in data1:
			record = Game(**{
				'id' : i[0],
				'name': i[1],
				'rating': i[2],
				'release_date': id[3],
				'deck': id[4],
				'concepts': id[5],
				'genres': id[6],
				'franchises': id[7],
				'description': id[8]
			})
			s.add(record)
		data2 = load_data(file_name[1])
		for i in data2:
			record = Company(**{
				'id' : i[0],
				'name': i[1],
				'founded_date': i[2],
				'address': i[3],
				'city': i[4],
				'country': i[5],
				'state': i[6],
				'deck': i[7],
				'concepts': i[8],
				'phone': i[9],
				'website': i[10],
				'description': i[11]
			})
			s.add(record)
		data3 = load_data(file_name[2])
		for i in data3:
			record = Platform(**{
				'id' : i[0],
				'name': i[1],
				'release_date': i[2],
				'online_support': id[3],
				'price': id[4],
				'company': id[5],
				'deck': id[6],
				'install_base': id[7],
				'description': id[8]
			})
	except:
		s.rollback()
	finally:
		s.close()