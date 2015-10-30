from db import *

if __name__ == "__main__":
    session = get_session(echo=True)
    migrate(session)
    session.commit()
    session.close()
