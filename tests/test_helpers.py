# -*- coding: utf-8 -*-

import datetime
import unittest

import chncal


class HelperTests(unittest.TestCase):
    def test_get_dates(self):
        cases = [
            ((2018, 2, 1), (2018, 1, 1), 0),
            ((2018, 1, 1), (2018, 1, 1), 1),
            ((2018, 1, 1), (2018, 1, 2), 2),
            ((2018, 1, 1), (2018, 2, 1), 32),
            ((2019, 1, 1), (2020, 1, 1), 366),
            ((2020, 1, 1), (2021, 1, 1), 367),
        ]
        for start, end, duration in cases:
            start, end = datetime.date(*start), datetime.date(*end)
            dates = chncal.get_dates(start, end)
            self.assertEqual(duration, len(dates))
            if dates:
                self.assertIn(start, dates)
                self.assertIn(end, dates)

    def test_get_workdays_holidays(self):
        cases = [
            ((2018, 2, 1), (2018, 1, 1), 0, 0, 0),
            ((2018, 1, 1), (2018, 1, 1), 1, 1, 0),
            ((2018, 1, 1), (2018, 1, 7), 3, 1, 4),
            ((2018, 1, 1), (2018, 2, 1), 9, 1, 23),
        ]
        for start, end, include_weekends, exclude_weekends, workdays in cases:
            start, end = datetime.date(*start), datetime.date(*end)
            self.assertEqual(include_weekends, len(chncal.get_holidays(start, end)))
            self.assertEqual(exclude_weekends, len(chncal.get_holidays(start, end, include_weekends=False)))
            self.assertEqual(workdays, len(chncal.get_workdays(start, end)))

    def test_find_workday(self):
        dates = [
            datetime.date(2017, 12, 30),
            datetime.date(2017, 12, 31),
            datetime.date(2018, 1, 1),
            datetime.date(2018, 1, 2),
        ]
        cases = [[chncal.find_workday(i, date) for i in range(-7, 7)] for date in dates]
        for i in range(len(cases) - 1):
            self.assertListEqual(cases[i], cases[i + 1])
