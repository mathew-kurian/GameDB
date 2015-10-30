from db import *

if __name__ == "__main__":
    session = get_session(echo=False)
    migrate(session)
    session.commit()
    session.close()
