from pydantic import BaseModel
from src.models.responses.embrapa_response import EmbrapaResponse
from src.models.embrapa.importation import Importation
from typing import List

class ImportacaoResponse(EmbrapaResponse, BaseModel):
    data: List[Importation]

    def __init__(self, data: List[Importation]):
        BaseModel.__init__(self)
        self.data = data

    @property
    def data(self):
        return self.data
    
    @property
    def set_data(self, data: List[Importation]):
        self.data = data