from pydantic import BaseModel

class Import(BaseModel):
    country: str
    kilograms: float
    dollars: float
    subroup: str
    year: int