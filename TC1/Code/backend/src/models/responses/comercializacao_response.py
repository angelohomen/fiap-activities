from pydantic import BaseModel
from src.models.responses.embrapa_response import EmbrapaResponse
from src.models.embrapa.trading import Trading
from typing import List

class ComercializacaoResponse(EmbrapaResponse, BaseModel):
    data: List[Trading]

    def __init__(self, data: List[Trading]):
        BaseModel.__init__(self)
        self.data = data

    @property
    def data(self):
        return self.data
    
    @property
    def set_data(self, data: List[Trading]):
        self.data = data