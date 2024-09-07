from pydantic import BaseModel
from src.models.responses.embrapa_response import EmbrapaResponse
from src.models.embrapa.production import Production
from typing import List

class ProducaoResponse(EmbrapaResponse, BaseModel):
    data: List[Production]

    def __init__(self, data: List[Production]):
        BaseModel.__init__(self)
        self.data = data

    @property
    def data(self):
        return self.data
    
    @property
    def set_data(self, data: List[Production]):
        self.data = data