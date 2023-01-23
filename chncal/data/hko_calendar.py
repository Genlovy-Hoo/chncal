# -*- coding: utf-8 -*-

'''
从香港天文台下载1901——2100年公历和农历转换对照表：
https://www.hko.gov.hk/tc/gts/time/conversion1_text.htm
更多天文历信息：
寿星天文历 http://www.nongli.net/sxwnl/
sxtwl https://github.com/yuangu/sxtwl_cpp
'''


import os
import re
import time
import warnings
import numpy as np
import pandas as pd
import urllib.request
from tqdm import tqdm

# https://www.bbsmax.com/A/amd0Gyoq5g/
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from dramkit.other import (load_text_multi,
                           traditional2simplified)
from dramkit.datetimetools import date_reformat_chn

from cn2an import cn2an


# # 干支纪年https://baike.baidu.com/item/干支纪年/3383226
# # 天干
# TG = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
# # 地支
# DZ = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
# # 属相
# SX = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
# k1, k2 = 0, 0
# TGDZ = [TG[k1]+DZ[k2]+'('+SX[k2]+')']
# while not (k1 == len(TG)-1 and  k2 == len(DZ)-1):
#     if k1 < len(TG)-1:
#         k1 += 1
#     else:
#         k1 = 0
#     if k2 < len(DZ)-1:
#         k2 += 1
#     else:
#         k2 = 0
#     TGDZ.append(TG[k1]+DZ[k2]+'('+SX[k2]+')')

TGDZ = ['甲子(鼠)', '乙丑(牛)', '丙寅(虎)', '丁卯(兔)',
        '戊辰(龙)', '己巳(蛇)', '庚午(马)', '辛未(羊)',
        '壬申(猴)', '癸酉(鸡)', '甲戌(狗)', '乙亥(猪)',
        '丙子(鼠)', '丁丑(牛)', '戊寅(虎)', '己卯(兔)',
        '庚辰(龙)', '辛巳(蛇)', '壬午(马)', '癸未(羊)',
        '甲申(猴)', '乙酉(鸡)', '丙戌(狗)', '丁亥(猪)',
        '戊子(鼠)', '己丑(牛)', '庚寅(虎)', '辛卯(兔)',
        '壬辰(龙)', '癸巳(蛇)', '甲午(马)', '乙未(羊)',
        '丙申(猴)', '丁酉(鸡)', '戊戌(狗)', '己亥(猪)',
        '庚子(鼠)', '辛丑(牛)', '壬寅(虎)', '癸卯(兔)',
        '甲辰(龙)', '乙巳(蛇)', '丙午(马)', '丁未(羊)',
        '戊申(猴)', '己酉(鸡)', '庚戌(狗)', '辛亥(猪)',
        '壬子(鼠)', '癸丑(牛)', '甲寅(虎)', '乙卯(兔)',
        '丙辰(龙)', '丁巳(蛇)', '戊午(马)', '己未(羊)',
        '庚申(猴)', '辛酉(鸡)', '壬戌(狗)', '癸亥(猪)']


def _check_hko_calendar_dir(save_dir=None):
    if pd.isnull(save_dir):
        nowdir = os.path.dirname(os.path.realpath(__file__))
        save_dir = os.path.join(nowdir, 'hko_calendar')
    return save_dir


def _download_hko_calendar(year,
                           save_dir=None,
                           force=False):
    save_dir = _check_hko_calendar_dir(save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, '%s.txt'%year)
    if force or (not os.path.exists(save_path)):
        url = 'https://www.hko.gov.hk/tc/gts/time/calendar/text/files/T%sc.txt'%year
        urllib.request.urlretrieve(url, save_path)
        
        
def download_hko_calendar(start_year=1901,
                          end_year=2100,
                          save_dir=None,
                          force=False):
    print('downloading hko calendar...')
    time.sleep(0.2)
    with tqdm(range(start_year, end_year+1)) as pbar:
        for year in pbar:
            _download_hko_calendar(year,
                                   save_dir=save_dir,
                                   force=force)
            # pbar.set_description(str(year))
            pbar.set_postfix(year=year)


class FileNotFoundWarning(Warning):
    pass


def load_hko_calendar(fpath):
    data = load_text_multi(fpath, encoding='big5hkscs')[0]
    if '2058' in fpath:
        d1 = data.columns[0]
        data = [d1] + data.iloc[:, 0].tolist()
    else:
        data = data.iloc[:, 0].tolist()
    data = [re.sub(r'\s+', ',', x) for x in data]
    data = [traditional2simplified(x) for x in data]
    data = [x for x in data if not '香港' in x]
    data = [x.split(',') for x in data]
    if '2058' in fpath:
        df = pd.DataFrame(data,
                    columns=['公历日期', '农历日期', '星期', '节气'])
    else:
        df = pd.DataFrame(data[1:], columns=data[0])
    return df


def _find_load_hko_calendar(year, save_dir=None):
    save_dir = _check_hko_calendar_dir(save_dir)
    fpath = os.path.join(save_dir, '%s.txt'%year)
    if not os.path.exists(fpath):
        warnings.warn('香港天文台%s年日历数据未找到！'%year,
                      category=FileNotFoundWarning)
        return pd.DataFrame(
                    columns=['公历日期', '农历日期', '星期', '节气'])   
    df = load_hko_calendar(fpath)
    return df
            
            
def find_load_hko_calendar(start_year=1901, end_year=2100,
                           save_dir=None):
    save_dir = _check_hko_calendar_dir(save_dir)
    save_path = os.path.join(save_dir, 'hko_calendar.csv')
    if not os.path.exists(save_path):
        print('\nloading hko calendar...')
        time.sleep(0.2)
        data = []
        with tqdm(range(start_year, end_year+1)) as pbar:
            for year in pbar:
                pbar.set_description(str(year))
                df = _find_load_hko_calendar(year, save_dir=save_dir)
                data.append(df)
        data = pd.concat(data, axis=0)
        data.reset_index(drop=True, inplace=True)
        data.to_csv(save_path, index=None, encoding='gbk')
    else:
        data = pd.read_csv(save_path, encoding='gbk')
    return data


def _get_tgdz_year(year):
    '''计算（农历）年份天干地支'''
    # 农历1984年是甲子年
    year = int(year)
    if year >= 1984:
        return TGDZ[(year-1984) % 60]
    else:
        return TGDZ[-((1984-year) % 60)]


def handle_hko_calendar(data, save_dir=None):
    '''
    | 香港天文台数据整理
    | 仅适用于data包含1901——2100年数据的情况
    '''
    df = data.copy()
    df['date'] = df['公历日期'].apply(lambda x: date_reformat_chn(x, '.'))
    df.sort_values('date', ascending=True, inplace=True)
    df['year'] = df['date'].apply(lambda x: x[:4])
    df['农历日'] = df['农历日期'].apply(lambda x: '初一' if '月' in x else x)
    df['农历d'] = df['农历日'].apply(lambda x: cn2an(x.replace('初', '')))
    df['农历月'] = df['农历日期'].apply(lambda x: x if '月' in x else np.nan)
    df['农历月'] = df['农历月'].fillna(method='ffill')
    df['农历月'] = df['农历月'].fillna('十一月')
    df['农历m'] = df['农历月'].apply(lambda x: cn2an(
        x.replace('正', '一').replace('闰', '').replace('月', '')))
    df['农历y'] = df[['year', '农历月']].apply(lambda x:
                    x['year'] if x['农历月'] == '正月' else np.nan,
                    axis=1)
    df['农历y'] = df['农历y'].fillna(method='ffill')
    df['农历y'] = df['农历y'].fillna(str(1900))
    df['农历月'] = df['农历月'].apply(lambda x:
                    x.replace('十一月', '冬月').replace('十二月', '腊月'))
    df['农历date_'] = df['农历y']+'年'+df['农历月']+df['农历日']
    df['农历date'] = df['农历y'] + '.' + \
                     df['农历m'].apply(lambda x: str(x).zfill(2)) + '.' + \
                     df['农历d'].apply(lambda x: str(x).zfill(2))
    df['农历date'] = df[['农历date', '农历date_']].apply(lambda x:
                     x['农历date']+'闰' if '闰' in x['农历date_'] else x['农历date'],
                     axis=1)
    # 公历节日
    festival = {
        '01.01': '元旦节',
        '02.14': '情人节',
        '05.01': '劳动节',
        '05.04': '青年节',
        '06.01': '儿童节',
        '09.10': '教师节',
        '10.01': '国庆节',
        '12.25': '圣诞节',
        '03.08': '妇女节',
        '03.12': '植树节',
        '04.01': '愚人节',
        '05.12': '护士节',
        '07.01': '建党节',
        '08.01': '建军节',
        '12.24': '平安夜',
    }
    df['公历节日'] = df['date'].apply(lambda x: festival[x[-5:]] \
                    if x[-5:] in festival else np.nan)
    # 农历节日
    lfestival = {
        '正月初一': '春节',
        '正月十五': '元宵节',
        '二月初二': '龙抬头',
        '五月初五': '端午节',
        '七月初七': '七夕节',
        '七月十五': '中元节',
        '八月十五': '中秋节',
        '九月初九': '重阳节',
        '十月初一': '寒衣节',
        '十月十五': '下元节',
        '腊月初八': '腊八节',
        '腊月廿三': '北方小年',
        '腊月廿四': '南方小年',
    }
    df['农历节日'] = df['农历date_'].apply(lambda x: lfestival[x[-4:]] \
                    if x[-4:] in lfestival and '闰' not in x else np.nan)
    # 除夕单独处理
    df['tmp'] = df['农历节日'].shift(-1)
    df['农历节日'] = df[['农历节日', 'tmp']].apply(lambda x:
                    '除夕' if x['tmp'] == '春节' else x['农历节日'], axis=1)
    df.drop('tmp', axis=1, inplace=True)
    # 星座
    def _get_xingzuo(md):
        '''获取星座'''
        if md >= '12.22' or md <= '01.19':
            return '摩羯座'
        elif '01.20' <= md <= '02.18':
            return '水瓶座'
        elif '02.19' <= md <= '03.20':
            return '双鱼座'
        elif '03.21' <= md <= '04.19':
            return '白羊座'
        elif '04.20' <= md <= '05.20':
            return '金牛座'
        elif '05.21' <= md <= '06.21':
            return '双子座'
        elif '06.22' <= md <= '07.22':
            return '巨蟹座'
        elif '07.23' <= md <= '08.22':
            return '狮子座'
        elif '08.23' <= md <= '09.22':
            return '处女座'
        elif '09.23' <= md <= '10.23':
            return '天秤座'
        elif '10.23' <= md <= '11.22':
            return '天蝎座'
        elif '11.23' <= md <= '12.21':
            return '射手座'
    df['星座'] = df['date'].apply(lambda x: _get_xingzuo(x[-5:]))
    # 干支纪年
    # # 按农历年份
    # df['干支年'] = df['农历y'].apply(_get_tgdz_year)
    # 按二十四节气（貌似属相按节气跨年才是正确的，即立春之后进入下一个属相年）
    gz_y = df[df['节气'] == '立春'][['date', '节气']].copy()
    gz_y['干支y'] = gz_y['date'].apply(lambda x: x[:4])
    df = pd.merge(df, gz_y[['date', '干支y']],
                  how='left', on='date')
    df['干支y'] = df['干支y'].fillna(method='ffill').fillna(method='bfill')
    df['干支年'] = df['干支y'].apply(_get_tgdz_year)
    # 干支纪月
    # 农历2018年大雪（冬月初一，公历2018.12.07）是甲子月
    solars = df[~df['节气'].isna()][['date', '节气']].copy()
    solars.loc[solars['date'] == '2018.12.07', '干支月'] = TGDZ[0]
    solars.reset_index(drop=True, inplace=True)
    i0 = solars[solars['date'] == '2018.12.07'].index[0]
    tmp1 = solars[solars.index >= i0].copy()
    tmp1['i'] = (tmp1.index - i0) // 2 % 60
    tmp1['干支月'] = tmp1['i'].apply(lambda x: TGDZ[x])
    tmp2 = solars[solars['date'] <= '2018.12.07'].copy()
    tmp2['i'] = (i0 - tmp2.index) // 2 % 60
    tmp2['i'] = tmp2['i'].shift(1)
    _0, _1 = tmp2['i'].dropna().iloc[:2]
    if _0 == _1:
        _0_ = int(_0+1) if int(_0) != 59 else 0 
    else:
        _0_ = int(_0)
    tmp2['i'].fillna(_0_, inplace=True)
    tmp2['干支月'] = tmp2['i'].apply(lambda x: TGDZ[-int(x)])
    solars = pd.concat((tmp2.iloc[:-1, :], tmp1), axis=0)
    df = pd.merge(df, solars[['date', '干支月']],
                  how='left', on='date')
    df['干支月'] = df['干支月'].fillna(method='ffill')
    first = df['干支月'].dropna().iloc[0]
    df['干支月'].fillna(TGDZ[TGDZ.index(first)-1], inplace=True)
    # 干支纪日
    # 农历2022年六月十二（公历2022.07.10）是甲子日
    datebase = pd.to_datetime('2022.07.10')
    df['干支日'] = pd.to_datetime(df['date']) - datebase
    df['干支日'] = df['干支日'].apply(lambda x: x.days)
    df['干支日'] = df['干支日'].apply(lambda x: TGDZ[x % 60] \
                    if x >= 0 else TGDZ[-(abs(x) % 60)])
    df['干支date'] = df['干支年']+'年,'+df['干支月']+'月,'+df['干支日']+'日'
    save_dir = _check_hko_calendar_dir(save_dir)
    save_path = os.path.join(save_dir, 'hko_calendar_handle.csv')
    df.to_csv(save_path, index=None, encoding='gbk')
    return df


if __name__ == '__main__':
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    download_hko_calendar(force=False)
    data = find_load_hko_calendar()
    df = handle_hko_calendar(data)
    
    tr.used()











        