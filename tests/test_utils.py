#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import (
    datetime,
    timedelta,
)

from pytz import timezone

from utils import (
    is_seven_o_clock_danish_time,
    is_in_previous_hour,
)


class TestUtilities():

    def test_is_seven_o_clock_true(self):
        seven_o_clock = datetime(2018, 11, 30, 7, 0, 0, 0, tzinfo=timezone("Europe/Copenhagen"))
        assert is_seven_o_clock_danish_time(seven_o_clock) == True

    def test_is_seven_o_clock_false(self):
        seven_o_clock = datetime(2018, 11, 30, 7, 0, 0, 0, tzinfo=timezone("UTC"))
        assert is_seven_o_clock_danish_time(seven_o_clock) == False

    def test_is_in_previous_hour_true(self):
        now = datetime.now()
        previous_hour_datetime = now - timedelta(hours=1)

        assert is_in_previous_hour(now, previous_hour_datetime) == True

    def test_is_in_previous_hour_false(self):
        now = datetime.now()
        previous_hour_datetime = now - timedelta(hours=2)

        assert is_in_previous_hour(now, previous_hour_datetime) == False

    def test_is_in_previous_hour_false_yesterday(self):
        now = datetime.now()
        previous_hour_datetime = now - timedelta(hours=24)

        assert is_in_previous_hour(now, previous_hour_datetime) == False
