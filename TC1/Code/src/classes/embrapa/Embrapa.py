# Imports
import requests
import warnings
import pandas as pd
import configparser
from datetime import datetime
from typing import Dict, List
from bs4 import BeautifulSoup
from src.classes.embrapa.utils.UrlValidate import UrlValidate
from src.classes.embrapa.utils.DataEngineering import DataEngineering

# Definitions
warnings.filterwarnings('ignore')
config = configparser.ConfigParser()
config.read('app.config')

class Embrapa(UrlValidate):

    EMBRAPA_URL: str = config['EMBRAPA']['URL']
    MIN_YEAR: int = 1970
    MAX_YEAR: int = datetime.today().year - 1

    def __init__(
        self
    ) -> None:
        super().__init__({
            'apresentacao': '01',
            'producao': '02',
            'processamento': '03',
            'comercializacao': '04',
            'importacao': '05',
            'exportacao': '06'
        })

    @classmethod
    def get_subtabs(
        cls,
        tab: str
    ) -> Dict[str, str]:
        tab: str = tab.lower()
        match tab:
            case 'processamento':
                return {
                    'viniferas': '01',
                    'americanas_e_hibridas': '02',
                    'uvas_de_mesa': '03',
                    'sem_classificacao': '04'
                }
            case 'importacao':
                return {
                    'vinhos_de_mesa': '01',
                    'espumantes': '02',
                    'uvas_frescas': '03',
                    'uvas_passas': '04',
                    'suco_de_uva': '05'
                }
            case 'exportacao':
                return {
                    'vinhos_de_mesa': '01',
                    'espumantes': '02',
                    'uvas_frescas': '03',
                    'suco_de_uva': '04'
                }
            case _:
                return {}

    @classmethod
    def __validate_years_inputs(
        cls,
        year_from: int,
        year_to: int
    ) -> bool:
        if year_from > year_to:
            return False
        if year_from > cls.MAX_YEAR:
            return False
        if year_to < cls.MIN_YEAR:
            return False
        return True
    
    def __get_df(
        self,
        tab: str,
        subtab: str,
        year_from: int,
        year_to: int,
        has_tabs: bool
    ) -> pd.DataFrame:
        to_ret: pd.DataFrame = pd.DataFrame()
        if not self.__validate_years_inputs(year_from, year_to):
            return to_ret
        subtabs: List[str] = []
        if subtab is not None:
            if not self.validate_subtab(tab, subtab):
                return to_ret
            subtabs = [subtab]
        else:
            if has_tabs:
                subtabs = self.get_subtabs(tab)
            else:
                subtabs = [None]
        for i in range(year_from, year_to + 1):
            for subtab in subtabs:
                url = self.get_request_url(tab, subtab, i)
                response = requests.get(url)
                response.raise_for_status()
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    table = soup.find('table', class_='tb_base tb_dados')
                    if table:
                        new_df = pd.read_html(str(table))[0]
                        if subtab:
                            new_df['subtab'] = subtab
                        new_df['Ano'] = i
                        to_ret = pd.concat([to_ret,new_df])
        return to_ret

    def get_producao_df(
        self,
        year_from: int = MIN_YEAR,
        year_to: int = MAX_YEAR
    ) -> pd.DataFrame:
        return DataEngineering.treat_producao_df(
            self.__get_df('producao', None, year_from, year_to, False)
        )
    
    def get_processamento_df(
        self,
        year_from: int = MIN_YEAR,
        year_to: int = MAX_YEAR,
        subtab: str = None
    ) -> pd.DataFrame:
        return DataEngineering.treat_processamento_df(
            self.__get_df('processamento', subtab, year_from, year_to, True)
        )
    
    def get_comercializacao_df(
        self,
        year_from: int = MIN_YEAR,
        year_to: int = MAX_YEAR
    ) -> pd.DataFrame:
        return DataEngineering.treat_comercializacao_df(
            self.__get_df('comercializacao', None, year_from, year_to, False)
        )
    
    def get_importacao_df(
        self,
        year_from: int = MIN_YEAR,
        year_to: int = MAX_YEAR,
        subtab: str = None
    ) -> pd.DataFrame:
        return DataEngineering.treat_importacao_df(
            self.__get_df('importacao', subtab, year_from, year_to, True)
        )
    
    def get_exportacao_df(
        self,
        year_from: int = MIN_YEAR,
        year_to: int = MAX_YEAR,
        subtab: str = None
    ) -> pd.DataFrame:
        return DataEngineering.treat_exportacao_df(
            self.__get_df('exportacao', subtab, year_from, year_to, True)
        )

    def get_request_url(
        self,
        tab: str,
        subtab: str = None,
        ano: int = MAX_YEAR
    ) -> str:
        tab: str = tab.lower()
        subtab: str = subtab.lower() if subtab is not None else subtab
        if not self.validate_tab_and_subtabs(tab, subtab):
            return None
        subtabs: str = self.get_subtabs(tab)
        url: str = self.EMBRAPA_URL+'index.php?'+f'ano={str(ano)}&'+('' if subtab is None else f'subopcao=subopt_{subtabs[subtab]}&')+f'opcao=opt_{self.tabs[tab]}'
        return url     