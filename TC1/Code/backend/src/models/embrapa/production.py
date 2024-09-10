from pydantic import BaseModel

class Production(BaseModel):
    product: str
    liters: float
    group: str
    year: int