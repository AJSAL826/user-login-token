from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine=create_engine("postgresql://postdb:postdb616@localhost:5432/btech")
Session=sessionmaker(bind=engine)


def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()