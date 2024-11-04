from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5433/ApiFilmes"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), unique=True)
    director = Column(String(50))
    year = Column(Integer)
    gender = Column(String(50))


Base.metadata.create_all(bind=engine) 

   



