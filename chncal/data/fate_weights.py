# -*- coding: utf-8 -*-

import pandas as pd
from cn2an import transform
from dramkit.iotools import pickle_file


def _trans_weight(df):
    df['重量'] = df['重量'].apply(lambda x: transform(
                 x.replace('两', '.')))
    df['重量'] = df['重量'].apply(lambda x:
                 x.replace('钱', '') if '.' in x else \
                 '0.'+x.replace('钱', ''))
    df['重量'] = df['重量'].apply(lambda x:
                                 str(round(float(x), 2)))
    return df


def handle_year(df_year):
    df = df_year.copy()
    df['干支']  = df['干支'] + '(' + df['属相'] + ')'
    df.drop('属相', axis=1, inplace=True)
    df = _trans_weight(df)
    return df


def handle_month(df_month):
    df = df_month.copy()
    df['月份'] = df['月份'].apply(lambda x: x.replace('正', '一').replace('冬', '十一').replace('腊', '十二'))
    df['月份'] = df['月份'].apply(lambda x: transform(x.replace('月', '')))
    df['月份'] = df['月份'].apply(lambda x: str(x).zfill(2))
    df = _trans_weight(df)
    return df


def handle_date(df_date):
    df = df_date.copy()
    df['日期'] = df['日期'].apply(lambda x: x.replace('初', '').replace('廿', '二十'))
    df['日期'] = df['日期'].apply(transform)
    df['日期'] = df['日期'].apply(lambda x: str(x).zfill(2))
    df = _trans_weight(df)
    return df


def handle_hour(df_date):
    df = df_date.copy()
    df['地支'] = df['地支'].apply(lambda x: x.replace('时', ''))
    df = _trans_weight(df)
    return df


def handle_song(df_song):
    df = df_song.copy()
    df['重量'] = df['重量'].apply(lambda x: x if x.endswith('两') else x+'钱')
    df = _trans_weight(df)
    return df


if __name__ == '__main__':
    df_year = pd.read_excel('./fate_weights/fate_weights.xlsx',
                            sheet_name='干支年')
    w_year = handle_year(df_year)
    
    
    df_month = pd.read_excel('./fate_weights/fate_weights.xlsx',
                             sheet_name='月(农历)')
    w_month = handle_month(df_month)
    
    
    df_date = pd.read_excel('./fate_weights/fate_weights.xlsx',
                             sheet_name='日(农历)')
    w_date = handle_date(df_date)
    
    
    df_hour = pd.read_excel('./fate_weights/fate_weights.xlsx',
                             sheet_name='时辰')
    w_hour = handle_hour(df_hour)
    
    
    df_song = pd.read_excel('./fate_weights/fate_weights.xlsx',
                             sheet_name='袁天罡称命歌')
    df_song = handle_song(df_song)
    
    
    data = {'w_year': w_year,
            'w_month': w_month,
            'w_date': w_date,
            'w_hour': w_hour,
            'song': df_song}
    pickle_file(data, './fate_weights/fate_weights')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





























