from enum import Enum

class EnumEmbrapaAPI(Enum):
    PRODUCAO: int = 1
    PROCESSAMENTO: int = 2
    IMPORTACAO: int = 3
    EXPORTACAO: int = 4
    COMERCIALIZACAO: int = 5