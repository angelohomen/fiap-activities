from pydantic import BaseModel
from src.models.responses.embrapa_response import EmbrapaResponse
from src.models.embrapa.exportation import Exportation
from typing import List

class ExportacaoResponse(EmbrapaResponse, BaseModel):
    data: List[Exportation]

    def __init__(self, data: List[Exportation]):
        BaseModel.__init__(self)
        self.data = data

    @property
    def data(self):
        return self.data
    
    @property
    def set_data(self, data: List[Exportation]):
        self.data = data