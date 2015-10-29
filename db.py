from sqlalchemy.orm import sessionmaker

from models import *


def get_session():
    engine = create_engine("mysql+pymysql://root:123456@localhost/idb?charset=utf8", echo=False)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


def test():
    session = get_session()

    print(to_json(session.query(Game).get(29935), sort_keys=True, indent=4))
    print(to_json(session.query(Company).get(1), sort_keys=True, indent=4))
    print(to_json(session.query(Platform).get(146), sort_keys=True, indent=4))

    session.close()


def migrate():
    def date_cast(a):
        if a:
            return datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%fZ")

    def drop_table(m, t):
        try:
            t.__table__.drop(m.bind)
        except:
            pass

    session = get_session()

    drop_table(session, GamePlatform)
    drop_table(session, GameCompany)
    drop_table(session, Game)
    drop_table(session, Platform)
    drop_table(session, Company)
    drop_table(session, Url)

    Base.metadata.create_all(session.bind)

    with open('scripts/giantbomb/csv/games.json') as f:
        for i in json.load(f):
            session.add(Game(**{
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
                'description': i['description']
            }))

    with open('scripts/giantbomb/csv/platforms.json') as f:
        for i in json.load(f):
            session.add(Platform(**{
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
            session.add(GameCompany(**{
                'game_id': i['game'],
                'company_id': i['company'],
                'role': i['relation']
            }))

    with open('scripts/giantbomb/csv/games-platforms.json') as f:
        for i in json.load(f):
            session.add(GamePlatform(**{
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
            session.add(Url(**{
                'entity_id': i['id'],
                'entity': i['relation'],
                'type': 'video',
                'source': i['video']
            }))

    session.commit()
    session.close()
