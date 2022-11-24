# -*- coding: utf-8 -*-

import pandas as pd
from dramkit.datetimetools import str2timestamp


if __name__ == '__main__':
    df = pd.read_csv('../solar_term_1899-2100.csv') # https://download.csdn.net/download/xin1324/14938532
    df['time'] = df['date'].astype(str)
    df['time'] = df['time'].apply(lambda x:
                 x[:4]+'-'+x[4:6]+'-'+x[6:8]+' '+\
                 x[8:10]+':'+x[10:12]+':'+x[12:])
    df = df[['ind', 'time', 'tag', 'year']]
    
    
    
    x = df[df['year'] == 2022].copy()
    x['t'] = x['time'].apply(str2timestamp)
    x['td'] = x['t'].diff() / (60*60*24)
