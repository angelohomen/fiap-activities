from pydantic import BaseModel

class Export(BaseModel):
    country: str
    kilograms: float
    dollars: float
    subroup: str
    year: int