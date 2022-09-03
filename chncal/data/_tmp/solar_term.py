# -*- coding: utf-8 -*-

import pandas as pd
from dramkit.datetimetools import str2timestamp


if __name__ == '__main__':
    df = pd.read_csv('../solar_term_1899-2100.csv')
    df['time'] = df['date'].astype(str)
    df['time'] = df['time'].apply(lambda x:
                 x[:4]+'-'+x[4:6]+'-'+x[6:8]+' '+\
                 x[8:10]+':'+x[10:12]+':'+x[12:])
    df = df[['ind', 'time', 'tag', 'year']]
    
    
    
    a = df[df['year'] == 2022].copy()
    a['t'] = a['time'].apply(str2timestamp)
    a['td'] = a['t'].diff() / (60*60*24)
