#!/usr/bin/env python3

from sqlalchemy.orm import sessionmaker

from models import *


def get_session(echo=True):
    engine = create_engine("mysql+pymysql://root:123456@localhost/idb?charset=utf8mb4", echo=echo)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


def to_dict(a):
    return json.loads(to_json(a))


def migrate(session=None):
    close = None

    if session is None:
        session = get_session()
        close = true

    def date_cast(a):
        if a:
            return datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%fZ")

    def drop_table(t):
        try:
            t.__table__.drop(session.bind)
        except:
            pass

    drop_table(GamePlatform)
    drop_table(GameCompany)
    drop_table(Game)
    drop_table(Platform)
    drop_table(Company)
    drop_table(Url)

    Base.metadata.create_all(session.bind)

    with open('scripts/giantbomb/csv/games.json') as f:
        session.add_all([Game(**{
            'id': i["id"],
            'name': i["name"],
            'rating': i["rating"],
            'release_date': date_cast(i["release_date"]),
            'deck': i["deck"],
            'concepts': i["concepts"],
            'genres': i["genres"],
            'franchises': i["franchises"],
            'description': i["description"]
        }) for i in json.load(f)])

    with open('scripts/giantbomb/csv/companies.json') as f:
        session.add_all([Company(**{
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
        }) for i in json.load(f)])

    with open('scripts/giantbomb/csv/platforms.json') as f:
        session.add_all([Platform(**{
            'id': i['id'],
            'name': i['name'],
            'release_date': date_cast(i['release_date']),
            'online_support': i['online_support'],
            'price': i['price'],
            'company': i['company'],
            'deck': i['deck'],
            'install_base': i['install_base'],
            'description': i['description']
        }) for i in json.load(f)])

    with open('scripts/giantbomb/csv/games-companies.json') as f:
        session.add_all([GameCompany(**{
            'game_id': i['game'],
            'company_id': i['company'],
            'role': i['relation']
        }) for i in json.load(f)])

    with open('scripts/giantbomb/csv/games-platforms.json') as f:
        session.add_all([GamePlatform(**{
            'platform_id': i['platform'],
            'game_id': i['game']
        }) for i in json.load(f)])

    with open('scripts/giantbomb/csv/images.json') as f:
        session.add_all([Url(**{
            'entity_id': i['id'],
            'entity': i['relation'],
            'type': 'image',
            'source': i['image']
        }) for i in json.load(f)])

    with open('scripts/giantbomb/csv/videos.json') as f:
        session.add_all([Url(**{
            'entity_id': i['id'],
            'entity': i['relation'],
            'type': 'video',
            'source': i['video']
        }) for i in json.load(f)])

    if close:
        session.commit()
        session.close()
