from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pathlib import Path

MAIN_PATH = Path(__file__).resolve().parent
DB_PATH = MAIN_PATH / 'db' / 'aufgabenbuch.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DB = f'sqlite:///{DB_PATH}'

engine = create_engine(DB,
                       connect_args={'check_same_thread': False}
                       )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()