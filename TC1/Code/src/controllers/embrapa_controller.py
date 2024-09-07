# Imports
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated

# Models
from src.models.responses.producao_response import ProducaoResponse
from src.models.responses.processamento_response import ProcessamentoResponse
from src.models.responses.importacao_response import ImportacaoResponse
from src.models.responses.exportacao_response import ExportacaoResponse
from src.models.responses.comercializacao_response import ComercializacaoResponse

# Repositories
from src.repositories.embrapa.embrapa import Embrapa
from src.repositories.db.sql_alchemy_db import Base, engine, SessionLocal
from src.repositories.auth import auth

# Instances
router = APIRouter(
    prefix='/embrapa',
    tags=['Embrapa']
)
ebp = Embrapa()

# Database
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

# HTTP exceptions
unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed.')
not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No data found.')

# Router
@router.get("/producao", status_code=status.HTTP_200_OK, response_model=ProducaoResponse, tags=["Embrapa"])
async def get_producao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    producao_df = ebp.get_producao_df(year_from=year_from, year_to=year_to)
    if len(producao_df.columns) < 1:
        raise not_found_exception
    return ProducaoResponse(producao_df.to_dict(orient='records'))

@router.get("/processamento", status_code=status.HTTP_200_OK, response_model=ProcessamentoResponse, tags=["Embrapa"])
async def get_processamento(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    processamento_df = ebp.get_processamento_df(year_from=year_from, year_to=year_to)
    if len(processamento_df.columns) < 1:
        raise not_found_exception
    return ProcessamentoResponse(processamento_df.to_dict(orient='records'))

@router.get("/importacao", status_code=status.HTTP_200_OK, response_model=ImportacaoResponse, tags=["Embrapa"])
async def get_importacao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    importacao_df = ebp.get_importacao_df(year_from=year_from, year_to=year_to)
    if len(importacao_df.columns) < 1:
        raise not_found_exception
    return ImportacaoResponse(importacao_df.to_dict(orient='records'))

@router.get("/exportacao", status_code=status.HTTP_200_OK, response_model=ExportacaoResponse, tags=["Embrapa"]
    )
async def get_exportacao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    exportacao_df = ebp.get_exportacao_df(year_from=year_from, year_to=year_to)
    if len(exportacao_df.columns) < 1:
        raise not_found_exception
    return ExportacaoResponse(exportacao_df.to_dict(orient='records'))

@router.get("/comercializacao", status_code=status.HTTP_200_OK, response_model=ComercializacaoResponse, tags=["Embrapa"])
async def get_comercializacao(
    user: user_dependency, db: db_dependency, year_from: int = Embrapa.MIN_YEAR, year_to: int = Embrapa.MAX_YEAR
):
    if user is None:
        raise unauthorized_exception
    comercializacao_df = ebp.get_comercializacao_df(year_from=year_from, year_to=year_to)
    if len(comercializacao_df.columns) < 1:
        raise not_found_exception
    return ComercializacaoResponse(comercializacao_df.to_dict(orient='records'))