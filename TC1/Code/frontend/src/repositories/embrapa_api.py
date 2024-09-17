# Imports
import os
import requests
from starlette import status
from dotenv import load_dotenv
from datetime import datetime

# Models
from src.models.enum_embrapa_api import EnumEmbrapaAPI

# Environment variables
load_dotenv()

class EmbrapaAPI():

    BASE_URL: str = os.getenv('BASE_URL')
    PRODUCAO = 'producao'
    PROCESSAMENTO = 'processamento'
    IMPORTACAO = 'importacao'
    EXPORTACAO = 'exportacao'
    COMERCIALIZACAO = 'comercializacao'

    def __init__(self, username: str, password: str) -> None:
        '''
            EmbrapaAPI is a class to manage embrapa-api requests.
        '''
        self.__token = None
        url = self.__route_construct('/auth/token')
        response = requests.post(url, data={
            'username': username,
            'password': password
        })
        if response.status_code == status.HTTP_200_OK:
            self.__token = response.json().get('access_token')
            self.__header = {
                'Authorization': f'Bearer {self.__token}'
            }
        else:
            raise Exception("Authentication error: ", response.status_code, response.text)

    @classmethod
    def __route_construct(cls, route: str) -> str:
        return cls.BASE_URL + route
    
    @property
    def token(self) -> str:
        return self.__token
    
    def get_user(self) -> str:
        '''
            Returns the authenticated user informations. 
        '''
        url = self.__route_construct('/auth/user')
        response = requests.get(url, headers=self.__header)
        if response.status_code == status.HTTP_200_OK:
            return response.json()
        else:
            raise Exception("Request error: ", response.status_code, response.text)
        
    def get_embrapa_data(
            self, 
            data: int,
            year_from: int = 1970,
            year_to: int = datetime.now().year - 1) -> str:
        '''
            Returns the reversed String.

            Parameters:
                data (str): Integer representing the wanted data (referenced on EnumEmbrapaAPI class).

            Returns:
                A json string representing the API response.   
        '''
        params = {
            'year_from': year_from,
            'year_to': year_to
        }
        if data == EnumEmbrapaAPI.COMERCIALIZACAO:
            response = requests.get(self.__route_construct('/embrapa/comercializacao'), params=params, headers=self.__header)
        elif data == EnumEmbrapaAPI.EXPORTACAO:
            response = requests.get(self.__route_construct('/embrapa/exportacao'), params=params, headers=self.__header)
        elif data == EnumEmbrapaAPI.IMPORTACAO:
            response = requests.get(self.__route_construct('/embrapa/importacao'), params=params, headers=self.__header)
        elif data == EnumEmbrapaAPI.PRODUCAO:
            response = requests.get(self.__route_construct('/embrapa/producao'), params=params, headers=self.__header)
        elif data == EnumEmbrapaAPI.PROCESSAMENTO:
            response = requests.get(self.__route_construct('/embrapa/processamento'), params=params, headers=self.__header)
        else:
            raise Exception("Input data not found.")
        if response.status_code == status.HTTP_200_OK:
            return response.json()
        else:
            raise Exception("Request error: ", response.status_code, response.text)