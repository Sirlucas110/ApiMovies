from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db.database import SessionLocal, Movie
from sqlalchemy.orm import Session
from model.movies import Movies

template = Jinja2Templates(directory="templates")




app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/filmes/register", response_class=HTMLResponse)
async def exibir_formulario(request: Request):
    return template.TemplateResponse("register.html", {"request": request})


@app.post("/filmes/register", response_model=Movies)
async def criar(db: db_dependency, title: str=Form(), director: str=Form(), year: int=Form(), gender: str=Form()):
    db_movies = Movie(title=title, director=director, year=year, gender=gender)
    db.add(db_movies)
    db.commit()
    db.refresh(db_movies)
    return db_movies

@app.get("/filmes", response_class=HTMLResponse)
async def buscar(db: db_dependency, request: Request):
    filmes = db.query(Movie).all()
    return template.TemplateResponse("filmes.html", {"request":request, "filmes": filmes})

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




