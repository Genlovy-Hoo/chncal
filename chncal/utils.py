# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import pandas as pd

from chncal.constants import holidays
from chncal.constants import in_lieu_days
from chncal.constants import workdays
from chncal.constants_atrade import atrade_calendar
from chncal.solar_terms import SolarTerms
from chncal.solar_terms import SOLAR_TERMS_C_NUMS
from chncal.solar_terms import SOLAR_TERMS_MONTH
from chncal.solar_terms import SOLAR_TERMS_DELTA


def _trans_date(date):
    if pd.isnull(date):
        date = datetime.datetime.now()
    if isinstance(date, str):
        date = pd.to_datetime(date)
    return date


def _wrap_date(date):
    '''
    transform datetime.datetime into datetime.date

    :type date: datetime.date | datetime.datetime
    :rtype: datetime.date
    '''
    date = _trans_date(date)
    if isinstance(date, datetime.datetime):
        date = date.date()
    return date


def _validate_date(*dates):
    '''
    check if the date(s) is supported

    :type date: datetime.date | datetime.datet'ime
    :rtype: datetime.date | list[datetime.date]
    '''
    if len(dates) != 1:
        return list(map(_validate_date, dates))
    date = _wrap_date(dates[0])
    if not isinstance(date, datetime.date):
        raise NotImplementedError('unsupported type {}, expected type is datetime.date'.format(type(date)))
    min_year, max_year = min(holidays.keys()).year, max(holidays.keys()).year
    if not (min_year <= date.year <= max_year):
        raise NotImplementedError(
            'no available data for year {}, only year between [{}, {}] supported'.format(date.year, min_year, max_year)
        )
    return date


def is_holiday(date):
    '''
    check if one date is holiday in China.
    in other words, Chinese people get rest at that day.

    :type date: datetime.date | datetime.datetime
    :rtype: bool
    '''
    return not is_workday(date)


def is_workday(date):
    '''
    check if one date is workday in China.
    in other words, Chinese people works at that day.

    :type date: datetime.date | datetime.datetime
    :rtype: bool
    '''
    date = _validate_date(date)
    weekday = date.weekday()
    return bool(date in workdays.keys() or (weekday <= 4 and date not in holidays.keys()))


def is_in_lieu(date):
    '''
    check if one date is in lieu in China.
    in other words, Chinese people get rest at that day because of legal holiday.

    :type date: datetime.date | datetime.datetime
    :rtype: bool
    '''
    date = _validate_date(date)
    return date in in_lieu_days


def get_holiday_detail(date):
    '''
    check if one date is holiday in China,
    and return the holiday name (None if it's a normal day)

    :type date: datetime.date | datetime.datetime
    :return: holiday bool indicator, and holiday name if it's holiday related day
    :rtype: (bool, str | None)
    '''
    date = _validate_date(date)
    if date in workdays.keys():
        return False, workdays[date]
    elif date in holidays.keys():
        return True, holidays[date]
    else:
        return date.weekday() > 4, None


def get_dates(start, end):
    '''
    get dates between start date and end date. (includes start date and end date)

    :type start: datetime.date | datetime.datetime
    :type end:  datetime.date | datetime.datetime
    :rtype: list[datetime.date]
    '''
    start, end = map(_wrap_date, (start, end))
    delta_days = (end - start).days
    return [start + datetime.timedelta(days=delta) for delta in range(delta_days + 1)]


def get_holidays(start, end, include_weekends=True):
    '''
    get holidays between start date and end date. (includes start date and end date)

    :type start: datetime.date | datetime.datetime
    :type end:  datetime.date | datetime.datetime
    :type include_weekends: bool
    :param include_weekends: False for excluding Saturdays and Sundays
    :rtype: list[datetime.date]
    '''
    start, end = _validate_date(start, end)
    if include_weekends:
        return list(filter(is_holiday, get_dates(start, end)))
    return list(filter(lambda x: x in holidays, get_dates(start, end)))


def get_workdays(start, end):
    '''
    get workdays between start date and end date. (includes start date and end date)

    :type start: datetime.date | datetime.datetime
    :type end:  datetime.date | datetime.datetime
    :rtype: list[datetime.date]
    '''
    start, end = _validate_date(start, end)
    return list(filter(is_workday, get_dates(start, end)))


def find_workday(delta_days=0, date=None):
    '''
    find the workday after {delta_days} days.

    :type delta_days: int
    :param delta_days: 0 means next workday (includes today), -1 means previous workday.
    :type date: datetime.date | datetime.datetime
    :param: the start point
    :rtype: datetime.date
    '''
    date = _wrap_date(date or datetime.date.today())
    if delta_days >= 0:
        delta_days += 1
    sign = 1 if delta_days >= 0 else -1
    for i in range(abs(delta_days)):
        if delta_days < 0 or i:
            date += datetime.timedelta(days=sign)
        while not is_workday(date):
            date += datetime.timedelta(days=sign)
    return date


def get_solar_terms(start, end):
    '''
    生成24节气
    通用寿星公式：https://www.jianshu.com/p/1f814c6bb475

    通式寿星公式：[Y×D+C]-L
    []里面取整数；Y=年数的后2位数；D=0.2422；L=Y/4，小寒、大寒、立春、雨水的 L=(Y-1)/4

    :type start: datetime.date
    :param start: 开始日期
    :type end: datetime.date
    :param end: 结束日期
    :rtype: list[(datetime.date, str)]
    '''
    start = _trans_date(start)
    end = _trans_date(end)
    if not 1900 <= start.year <= 2100 or not 1900 <= end.year <= 2100:
        raise NotImplementedError('only year between [1900, 2100] supported')
    D = 0.2422
    result = []
    year, month = start.year, start.month
    while year < end.year or (year == end.year and month <= end.month):
        # 按月计算节气
        for solar_term in SOLAR_TERMS_MONTH[month]:
            nums = SOLAR_TERMS_C_NUMS[solar_term]
            C = nums[0] if year < 2000 else nums[1]
            # 2000 年的小寒、大寒、立春、雨水按照 20 世纪的 C 值来算
            if year == 2000 and solar_term in [
                SolarTerms.lesser_cold,
                SolarTerms.greater_cold,
                SolarTerms.the_beginning_of_spring,
                SolarTerms.rain_water,
            ]:
                C = nums[0]
            Y = year % 100
            L = int(Y / 4)
            if solar_term in [
                SolarTerms.lesser_cold,
                SolarTerms.greater_cold,
                SolarTerms.the_beginning_of_spring,
                SolarTerms.rain_water,
            ]:
                L = int((Y - 1) / 4)
            day = int(Y * D + C) - L
            # 计算偏移量
            delta = SOLAR_TERMS_DELTA.get((year, solar_term))
            if delta:
                day += delta
            _date = datetime.date(year, month, day)
            if _date < start or _date > end:
                continue
            result.append((_date, solar_term.value[1]))
        if month == 12:
            year, month = year + 1, 1
        else:
            month += 1
    return result


def get_recent_workday(date=None, dirt='post'):
    '''
    若date为工作日，则返回，否则返回下一个(post)或上一个(pre)工作日
    '''
    date = _trans_date(date)
    tdelta = datetime.timedelta(1)
    if dirt == 'post':
        while not is_workday(date):
            date =  date + tdelta
    elif dirt == 'pre':
        while not is_workday(date):
            date =  date - tdelta
    return _wrap_date(date)


def get_next_nth_workday(date=None, n=1):
    '''
    | 给定日期date，返回其后第n个工作日日期，n可为负数（返回结果在date之前）
    | 若n为0，直接返回date
    '''
    date = _trans_date(date)
    n_add = -1 if n < 0 else 1
    n = abs(n)
    tmp = 0
    while tmp < n:
        date = date = date + datetime.timedelta(n_add)
        if is_workday(date):
            tmp += 1
    return _wrap_date(date)


def get_work_dates(start_date, end_date=None):
    '''
    取指定起止日期内的工作日
    '''
    start_date = _trans_date(start_date)
    end_date = _trans_date(end_date)
    dates = get_workdays(start_date, end_date)
    dates = [_wrap_date(x) for x in dates]
    return dates


def _is_tradeday(date):
    return is_workday(date) and date.weekday() not in [5, 6]


def is_tradeday(date=None):
    '''判断是否为沪深A股交易日'''
    date = _wrap_date(date)
    if date in atrade_calendar:
        return bool(atrade_calendar[date])
    return _is_tradeday(date)


def get_recent_tradeday(date=None, dirt='post'):
    '''
    若date为交易日，则直接返回date，否则返回下一个(dirt='post')或上一个(dirt='pre')交易日
    '''
    assert dirt in ['post', 'pre']
    date = _trans_date(date)
    tdelta = datetime.timedelta(1)
    if dirt == 'post':
        while not is_tradeday(date):
            date = date + tdelta
    elif dirt == 'pre':
        while not is_tradeday(date):
            date = date - tdelta
    return _wrap_date(date)


def get_next_nth_tradeday(date=None, n=1):
    '''
    | 给定日期date，返回其后第n个交易日日期，n可为负数（返回结果在date之前）
    | 若n为0，直接返回date
    '''
    date = _trans_date(date)
    n_add = -1 if n < 0 else 1
    n = abs(n)
    tmp = 0
    while tmp < n:
        date = date + datetime.timedelta(n_add)
        if is_tradeday(date):
            tmp += 1
    return _wrap_date(date)


def get_trade_dates(start_date, end_date=None):
    '''
    取指定起止日期内的交易日期（周内的工作日）
    '''
    start_date = _trans_date(start_date)
    end_date = _trans_date(end_date)
    dates = pd.date_range(start_date, end_date)
    dates = [x for x in dates if is_tradeday(x)]
    dates = [_wrap_date(x) for x in dates]
    return dates
