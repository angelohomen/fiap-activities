from pydantic import BaseModel

class Trading(BaseModel):
    product: str
    liters: float
    group: str
    year: int