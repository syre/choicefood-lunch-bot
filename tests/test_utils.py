#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pytz import timezone

from lunchbot.utils import (
    is_seven_o_clock_danish_time,
    is_in_previous_hour,
    add_formatting,
    remove_excessive_newlines,
)

class TestUtilities():

    def test_is_seven_o_clock_true(self):
        seven_o_clock = datetime(2018, 11, 30, 7, 0, 0, 0, tzinfo=timezone("Europe/Copenhagen"))
        assert is_seven_o_clock_danish_time(seven_o_clock) == True
    
    def test_is_seven_o_clock_false(self):
        seven_o_clock = datetime(2018, 11, 30, 7, 0, 0, 0, tzinfo=timezone("UTC"))
        assert is_seven_o_clock_danish_time(seven_o_clock) == False