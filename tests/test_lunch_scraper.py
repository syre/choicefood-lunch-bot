#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from lunchbot.lunch_scraper import (
    get_week_pattern,
)


class TestLunchScraper():

    def test_get_week_pattern(self):
        # wednesday week 5
        test_date = datetime(2019, 1, 30)

        week_pattern = get_week_pattern(test_date)
        assert week_pattern == "uge 5"

    def test_get_week_pattern_weekend_get_next_week(self):
        # saturday week 5
        test_date = datetime(2019, 2, 2)
        week_pattern = get_week_pattern(test_date)
        assert week_pattern == "uge 6"
