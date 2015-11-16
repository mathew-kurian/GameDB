#!/usr/bin/env python3
import gc

from sqlalchemy.orm import sessionmaker

from models import *
import ijson


def get_session(echo=True):
    """
    Create a sql session with debugging on/off
    """
    engine = create_engine("mysql+pymysql://root:123456@localhost/idb?charset=utf8mb4", echo=echo)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


def to_dict(a):
    """
    Convert model to json
    """
    return json.loads(to_json(a))


def migrate(session=None):
    """
    Import collected info into sql 
    """
    close = None

    if session is None:
        session = get_session(False)
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

    with open('scripts/giantbomb/json/games.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(Game(**{
                'id': i["id"],
                'name': i["name"],
                'rating': i["rating"],
                'release_date': date_cast(i["release_date"]),
                'deck': i["deck"],
                'concepts': i["concepts"],
                'genres': i["genres"],
                'franchises': i["franchises"],
                'description': i["description"],
                'entity' : 'game'
            }))

        f.close()

    gc.collect()
    print('finished games.json')

    if close:
        session.commit()

    with open('scripts/giantbomb/json/companies.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(Company(**{
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
                'description': i['description'],
                'entity': 'company'
            }))

    gc.collect()
    print('finished companies.json')

    if close:
        session.commit()

    with open('scripts/giantbomb/json/platforms.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(Platform(**{
                'id': i['id'],
                'name': i['name'],
                'release_date': date_cast(i['release_date']),
                'online_support': i['online_support'],
                'price': i['price'],
                'company': i['company'],
                'deck': i['deck'],
                'install_base': i['install_base'],
                'description': i['description'],
                'entity': 'platform'
            }))

    gc.collect()
    print('finished platforms.json')

    if close:
        session.commit()

    with open('scripts/giantbomb/json/games-companies.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(GameCompany(**{
                'game_id': i['game'],
                'company_id': i['company'],
                'role': i['relation']
            }))

    gc.collect()
    print('finished games-companies.json')

    if close:
        session.commit()

    with open('scripts/giantbomb/json/games-platforms.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(GamePlatform(**{
                'platform_id': i['platform'],
                'game_id': i['game']
            }))

    gc.collect()
    print('finished games-platforms.json')

    if close:
        session.commit()

    with open('scripts/giantbomb/json/images.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(Url(**{
                'entity_id': i['id'],
                'entity': i['relation'],
                'type': 'image',
                'source': i['image']
            }))

    gc.collect()
    print('finished images.json')

    if close:
        session.commit()

    with open('scripts/giantbomb/json/videos.json') as f:
        for i in ijson.items(f, 'item'):
            session.add(Url(**{
                'entity_id': i['id'],
                'entity': i['relation'],
                'type': 'video',
                'source': i['video']
            }))

    gc.collect()
    print('finished videos.json')

    if close:
        session.commit()
        session.close()
