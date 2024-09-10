from pydantic import BaseModel
from src.models.responses.embrapa_response import EmbrapaResponse
from src.models.embrapa.processing import Processing
from typing import List

class ProcessamentoResponse(EmbrapaResponse, BaseModel):
    data: List[Processing]

    def __init__(self, data: List[Processing]):
        BaseModel.__init__(self)
        self.data = data

    @property
    def data(self):
        return self.data
    
    @property
    def set_data(self, data: List[Processing]):
        self.data = data