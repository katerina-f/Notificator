from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config
from notificator.user.model import Base

config = Config()


class DatabaseInstance:
    def __init__(self):
        self.engine = create_engine(config.SQLALCHEMY_BASE_URI)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def create_db(self):
        Base.metadata.create_all(self.engine)


db = DatabaseInstance()
