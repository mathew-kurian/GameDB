from datetime import datetime
from models import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import json


def date_cast(a):
    if a:
        return datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%fZ")


def drop_table(e, t):
    try:
        t.__table__.drop(e)
    except:
        pass


if __name__ == "__main__":
    engine = create_engine("mysql+pymysql://root:123456@localhost/idb?charset=utf8", echo=True)

    session = sessionmaker()
    session.configure(bind=engine)

    s = session()

    drop_table(engine, GamePlatform)
    drop_table(engine, GameCompany)
    drop_table(engine, Game)
    drop_table(engine, Platform)
    drop_table(engine, Company)
    drop_table(engine, Url)

    Base.metadata.create_all(engine)

    with open('scripts/giantbomb/csv/games.json') as f:
        for i in json.load(f):
            s.add(Game(**{
                'id': i["id"],
                'name': i["name"],
                'rating': i["rating"],
                'release_date': date_cast(i["release_date"]),
                'deck': i["deck"],
                'concepts': i["concepts"],
                'genres': i["genres"],
                'franchises': i["franchises"],
                'description': i["description"]
            }))

    with open('scripts/giantbomb/csv/companies.json') as f:
        for i in json.load(f):
            s.add(Company(**{
                'id': i['id'],
                'name': i['name'],
                'founded_date': date_cast(i['founded_date']),
                'address': i['address'],
                'city': i['city'],
                'country': i['country'],
                'state': i['state'],
                'deck': i['deck'],
                'concepts': i['concepts'],
                'phone': i['phone'],
                'website': i['website'],
                'description': i['description']
            }))

    with open('scripts/giantbomb/csv/platforms.json') as f:
        for i in json.load(f):
            s.add(Platform(**{
                'id': i['id'],
                'name': i['name'],
                'release_date': date_cast(i['release_date']),
                'online_support': i['online_support'],
                'price': i['price'],
                'company': i['company'],
                'deck': i['deck'],
                'install_base': i['install_base'],
                'description': i['description']
            }))

    with open('scripts/giantbomb/csv/games-companies.json') as f:
        for i in json.load(f):
            s.add(GameCompany(**{
                'game_id': i['game'],
                'company_id': i['company'],
                'role': i['relation']
            }))

    with open('scripts/giantbomb/csv/games-platforms.json') as f:
        for i in json.load(f):
            s.add(GamePlatform(**{
                'platform_id': i['platform'],
                'game_id': i['game']
            }))

    # with open('scripts/giantbomb/csv/images.json') as f:
    #     for i in json.load(f):
    #         s.add( Url(**{
    #             'entity_id': i['id'],
    #             'entity': i['relation'],
    #             'type': 'image',
    #             'source': i['image']
    #         }))

    with open('scripts/giantbomb/csv/videos.json') as f:
        for i in json.load(f):
            s.add(Url(**{
                'entity_id': i['id'],
                'entity': i['relation'],
                'type': 'video',
                'source': i['video']
            }))

    s.commit()
    s.close()
