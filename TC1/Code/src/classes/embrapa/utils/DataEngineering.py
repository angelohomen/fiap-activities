# Imports
import pandas as pd
from unidecode import unidecode

class DataEngineering:

    @classmethod
    def treat_producao_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Produto']!='Total']
            df['Grupo'] = df['Produto'].where(df['Produto'].str.isupper())
            df['Grupo'] = df['Grupo'].ffill()
            df = df[~df['Produto'].str.isupper()]
            df['Quantidade (L.)'] = df['Quantidade (L.)'].replace('-', '0').str.replace('.', '', regex=False).astype(float)
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
        df = df.copy()
        if len(df.columns) > 0:
            df.drop('Sem definição', axis=1, inplace=True)
            df = df[df['Cultivar']!='Total']
            df = df.dropna()
            df['Grupo'] = df['Cultivar'].where(df['Cultivar'].str.isupper())
            df['Grupo'] = df['Grupo'].ffill()
            df = df[~df['Cultivar'].str.isupper()]
            df['Quantidade (Kg)'] = df['Quantidade (Kg)'].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
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
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Produto']!='Total']
            df['Grupo'] = df['Produto'].where(df['Produto'].str.isupper())
            df['Grupo'] = df['Grupo'].ffill()
            df = df[~df['Produto'].str.isupper()]
            df['Quantidade (L.)'] = df['Quantidade (L.)'].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
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
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Países']!='Total']
            df['Quantidade (Kg)'] = df['Quantidade (Kg)'].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
            df['Valor (US$)'] = df['Valor (US$)'].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
            df['Países'] = cls.default_string_column(df, 'Países')
            df.columns = ['country','kilograms','dollars','subgroup','year']
        return df

    @classmethod
    def treat_exportacao_df(
        cls,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        df = df.copy()
        if len(df.columns) > 0:
            df = df[df['Países']!='Total']
            df['Quantidade (Kg)'] = df['Quantidade (Kg)'].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
            df['Valor (US$)'] = df['Valor (US$)'].replace('-', '0').replace('nd', '0').replace('*', '0').str.replace('.', '', regex=False).astype(float)
            df['Países'] = cls.default_string_column(df, 'Países')
            df.columns = ['country','kilograms','dollars','subgroup','year']
        return df
    
    @classmethod
    def default_string_column(
        cls,
        df: pd.DataFrame,
        col: str
    ) -> pd.Series:
        to_ret: pd.DataFrame = df
        if col not in df.columns:
            return to_ret
        to_ret[col] = to_ret[col].str.replace(r'[()]', '', regex=True).str.replace(r'[^a-zA-Z0-9\s]', '', regex=True).str.replace(' ', '_', regex=False).apply(unidecode).str.lower()
        return to_ret[col]