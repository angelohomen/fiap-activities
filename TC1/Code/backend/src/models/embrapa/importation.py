from pydantic import BaseModel

class Importation(BaseModel):
    country: str
    kilograms: float
    dollars: float
    subroup: str
    year: int