from fastapi import FastAPI, Depends, HTTPException, status
from src.repositories.auth import auth
from sqlalchemy.orm import Session
from typing import Annotated

# models
from src.models.embrapa.production import Production
from src.models.embrapa.processing import Processing
from src.models.embrapa.importation import Import
from src.models.embrapa.exportation import Export
from src.models.embrapa.trading import Trading

# repositories
from src.repositories.embrapa.embrapa import Embrapa
from src.repositories.db.sql_alchemy_db import Base, engine, SessionLocal
from typing import List

app = FastAPI()
app.include_router(auth.router)

ebp = Embrapa()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')

@app.get("/user", status_code=status.HTTP_200_OK, tags=['User'])
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise unauthorized_exception
    return {'User': user}

@app.get("/embrapa/producao", status_code=status.HTTP_200_OK, response_model=List[Production], tags=["Embrapa"]
    )
async def get_producao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    return ebp.get_producao_df(year_from=year_from, year_to=year_to).to_dict(orient='records')

@app.get("/embrapa/processamento", status_code=status.HTTP_200_OK, response_model=List[Processing], tags=["Embrapa"])
async def get_processamento(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    return ebp.get_processamento_df(year_from=year_from, year_to=year_to).to_dict(orient='records')

@app.get("/embrapa/importacao", status_code=status.HTTP_200_OK, response_model=List[Import], tags=["Embrapa"])
async def get_importacao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    return ebp.get_importacao_df(year_from=year_from, year_to=year_to).to_dict(orient='records')

@app.get("/embrapa/exportacao", status_code=status.HTTP_200_OK, response_model=List[Export], tags=["Embrapa"]
    )
async def get_exportacao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    return ebp.get_exportacao_df(year_from=year_from, year_to=year_to).to_dict(orient='records')

@app.get("/embrapa/comercializacao", status_code=status.HTTP_200_OK, response_model=List[Trading], tags=["Embrapa"])
async def get_comercializacao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    return ebp.get_comercializacao_df(year_from=year_from, year_to=year_to).to_dict(orient='records')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
