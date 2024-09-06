# Imports
import pandas as pd
from unidecode import unidecode

class DataEngineering:

    @classmethod
    def treat_producao_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        '''
            Normalize raw "producao" dataframe.
        '''
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Produto']!='Total']
            df['Grupo'] = df['Produto'].where(df['Produto'].str.isupper())
            df['Grupo'] = df['Grupo'].ffill()
            df = df[~df['Produto'].str.isupper()]
            df['Quantidade (L.)'] = cls.default_float_column(df, 'Quantidade (L.)')
            df['Produto'] = cls.default_string_column(df, 'Produto')
            df['Grupo'] = cls.default_string_column(df, 'Grupo')
            df.columns = ['product','liters','year','group']
            df = df[['product','liters','group','year']]
        return df

    @classmethod
    def treat_processamento_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        '''
            Normalize raw "processamento" dataframe.
        '''
        df = df.copy()
        if len(df.columns) > 0:
            df.drop('Sem definição', axis=1, inplace=True)
            df = df[df['Cultivar']!='Total']
            df = df.dropna()
            df['Grupo'] = df['Cultivar'].where(df['Cultivar'].str.isupper())
            df['Grupo'] = df['Grupo'].ffill()
            df = df[~df['Cultivar'].str.isupper()]
            df['Quantidade (Kg)'] = cls.default_float_column(df, 'Quantidade (Kg)')
            df['Cultivar'] = cls.default_string_column(df, 'Cultivar')
            df['Grupo'] = cls.default_string_column(df, 'Grupo')
            df.columns = ['cultivate','kilograms','subgroup','year','group']
            df = df[['cultivate','kilograms','group','subgroup','year']]
        return df

    @classmethod
    def treat_comercializacao_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        '''
            Normalize raw "comercializacao" dataframe.
        '''
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Produto']!='Total']
            df['Grupo'] = df['Produto'].where(df['Produto'].str.isupper())
            df['Grupo'] = df['Grupo'].ffill()
            df = df[~df['Produto'].str.isupper()]
            df['Quantidade (L.)'] = cls.default_float_column(df, 'Quantidade (L.)')
            df['Produto'] = cls.default_string_column(df, 'Produto')
            df['Grupo'] = cls.default_string_column(df, 'Grupo')
            df.columns = ['product','liters','year','group']
            df = df[['product','liters','group','year']]
        return df

    @classmethod
    def treat_importacao_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        '''
            Normalize raw "importacao" dataframe.
        '''
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Países']!='Total']
            df['Quantidade (Kg)'] = cls.default_float_column(df, 'Quantidade (Kg)')
            df['Valor (US$)'] = cls.default_float_column(df, 'Valor (US$)')
            df['Países'] = cls.default_string_column(df, 'Países')
            df.columns = ['country','kilograms','dollars','subgroup','year']
        return df

    @classmethod
    def treat_exportacao_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        '''
            Normalize raw "exportacao" dataframe.
        '''
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Países']!='Total']
            df['Quantidade (Kg)'] = cls.default_float_column(df, 'Quantidade (Kg)')
            df['Valor (US$)'] = cls.default_float_column(df, 'Valor (US$)')
            df['Países'] = cls.default_string_column(df, 'Países')
            df.columns = ['country','kilograms','dollars','subgroup','year']
        return df
    
    @classmethod
    def default_string_column(
        cls,
        df: pd.DataFrame,
        col: str
    ) -> pd.Series:
        '''
            Normalize strings without any special character.
        '''
        to_ret: pd.DataFrame = df
        if col not in df.columns:
            return to_ret
        to_ret[col] = to_ret[col].str.replace(r'[()]', '', regex=True).str.replace(' ', '_', regex=False).apply(unidecode).str.lower()
        return to_ret[col]
    
    @classmethod
    def default_float_column(
        cls,
        df: pd.DataFrame,
        col: str
    ) -> pd.Series:
        '''
            Normalize float without any special character.
        '''
        to_ret: pd.DataFrame = df
        if col not in df.columns:
            return to_ret
        to_ret[col] = to_ret[col].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
        return to_ret[col]