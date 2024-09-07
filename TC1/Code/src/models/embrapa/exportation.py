from pydantic import BaseModel

class Exportation(BaseModel):
    country: str
    kilograms: float
    dollars: float
    subroup: str
    year: int