#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime
import os
from sqlalchemy import create_engine

def month_to_number(x):
    if(x.MES == 'Jan'):
        return 1
    elif(x.MES == 'Fev'):
        return 2
    elif(x.MES == 'Mar'):
        return 3
    elif(x.MES == 'Abr'):
        return 4
    elif(x.MES == 'Mai'):
        return 5
    elif(x.MES == 'Jun'):
        return 6
    elif(x.MES == 'Jul'):
        return 7
    elif(x.MES == 'Ago'):
        return 8
    elif(x.MES == 'Set'):
        return 9
    elif(x.MES == 'Out'):
        return 10
    elif(x.MES == 'Nov'):
        return 11
    elif(x.MES == 'Dez'):
        return 12


xls = pd.ExcelFile(os.getcwd()+'/app/Vendas_de_Combustiveis_m3_todos_anos.xls')
timestamp_captura = datetime.datetime.now()

df_concatenado = pd.DataFrame()
for i in xls.sheet_names:
    if(i != 'Plan1'):
        df_temp = pd.read_excel(xls,i)
        df_temp = df_temp.drop(['TOTAL'], axis=1)
        df_temp = df_temp.melt(id_vars=['COMBUSTÍVEL','ANO','REGIÃO','ESTADO','UNIDADE'],
                                var_name='MES', value_name='VALOR')
        frames =[df_concatenado,df_temp]
        df_concatenado = pd.concat(frames)
    else:
        df_compare = pd.read_excel(xls,i)
df_concatenado['timestamp_captura'] = timestamp_captura

print('Prévia de resultados:')
print(df_concatenado.head(10))

df_concatenado.to_csv(os.getcwd()+'/app/df_resultado.csv')
df_concatenado['MES'] = df_concatenado.apply(month_to_number,axis=1)

conn_uri = 'postgresql+psycopg2://test:test@db/test'
psql_engine = create_engine(conn_uri)
df_concatenado.to_sql(name='vendas_de_combustiveis', con=psql_engine,
                       if_exists='replace',chunksize=1000,schema='public',
                        method='multi',index=False)
print('Dataframe carregado no banco')
