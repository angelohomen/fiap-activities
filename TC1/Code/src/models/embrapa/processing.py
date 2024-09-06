from pydantic import BaseModel

class Processing(BaseModel):
    cultivate: str
    kilograms: float
    group: str
    subgroup: str
    year: int