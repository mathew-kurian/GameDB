from sqlalchemy.orm import sessionmaker
from models import *

if __name__ == "__main__":
    engine = create_engine("mysql+pymysql://root:123456@localhost/idb?charset=utf8", echo=False)

    session = sessionmaker()
    session.configure(bind=engine)

    s = session()

    print(to_json(s.query(Game).get(29935), sort_keys=True, indent=4))
    print(to_json(s.query(Company).get(1), sort_keys=True, indent=4))
    print(to_json(s.query(Platform).get(146), sort_keys=True, indent=4))

    s.close()
