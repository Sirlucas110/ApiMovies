from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException
from db.database import SessionLocal, Movie
from sqlalchemy.orm import Session
from model.movies import Movies




app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/filmes", response_model=Movies)
async def criar(filme: Movies, db: db_dependency):
    db_movies = Movie(title=filme.title, director=filme.director, year=filme.year, gender=filme.gender)
    db.add(db_movies)
    db.commit()
    db.refresh(db_movies)
    return db_movies

@app.get("/filmes", response_model=List[Movies])
async def buscar(db: db_dependency):
    fillmes = db.query(Movie).all()
    return fillmes

@app.put("/filmes/{id}", response_model=Movies)
async def atualizar(id: int, filme: Movies, db: db_dependency):
    novo = db.query(Movie).filter(Movie.id == id).first()

    if novo is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")


    novo.title = filme.title
    novo.director = filme.director
    novo.year = filme.year
    novo.gender = filme.gender

    db.commit()
    db.refresh(novo)
    return novo

@app.delete("/filmes/{id}")
async def remover(id: int, db: db_dependency):
    try:
        db.query(Movie).filter(Movie.id == id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    return "Filme removido com sucesso"




