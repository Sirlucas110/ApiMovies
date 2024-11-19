from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db.database import SessionLocal, Movie
from model.movies import Movies

template = Jinja2Templates(directory="templates")

app = FastAPI()

# Gerenciador de sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Montagem de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Exibição do formulário de registro
@app.get("/filmes/register", response_class=HTMLResponse)
async def exibir_formulario(request: Request):
    return template.TemplateResponse("register.html", {"request": request})

# Criação de um novo filme
@app.post("/filmes/register", response_model=Movies)
async def criar_filme(db: db_dependency, title: str = Form(), director: str = Form(), year: int = Form(), gender: str = Form()):
    novo_filme = Movie(title=title, director=director, year=year, gender=gender)
    db.add(novo_filme)
    db.commit()
    db.refresh(novo_filme)
    return novo_filme

# Listagem de filmes
@app.get("/filmes", response_class=HTMLResponse)
async def listar_filmes(db: db_dependency, request: Request):
    filmes = db.query(Movie).all()
    return template.TemplateResponse("filmes.html", {"request": request, "filmes": filmes})

@app.get("/filmes/edit/{id}", response_class=HTMLResponse)
async def editar_formulario(id: int, db: db_dependency, request: Request):
    filme = db.query(Movie).filter(Movie.id == id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return template.TemplateResponse("edit.html", {"request": request, "filme": filme})


# Atualização de um filme
@app.post("/filmes/edit/{id}", response_class=HTMLResponse)
async def editar_filme(
    id: int,
    db: db_dependency,
    request: Request,
    title: str = Form(),
    director: str = Form(),
    year: int = Form(),
    gender: str = Form()
):
    filme = db.query(Movie).filter(Movie.id == id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    filme.title = title
    filme.director = director
    filme.year = year
    filme.gender = gender

    db.commit()
    db.refresh(filme)
    filmes = db.query(Movie).all()
    return template.TemplateResponse("filmes.html", {"request": request, "filmes": filmes})




# Remoção de um filme
@app.post("/filmes/delete/{id}", response_class=HTMLResponse)
async def deletar_filme(id: int, db: db_dependency, request: Request):
    filme = db.query(Movie).filter(Movie.id == id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    db.delete(filme)
    db.commit()
    
    filmes = db.query(Movie).all()
    return template.TemplateResponse("filmes.html", {"request": request, "filmes": filmes})
