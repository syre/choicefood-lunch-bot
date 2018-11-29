#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module containing various utilities for the lunch bot.
"""
from datetime import (
    datetime,
    timedelta,
)
from pytz import timezone

def is_seven_o_clock_danish_time():
    """Check if datetime is seven o clock in the morning in Denmark."""
    now = datetime.now(
        tz=timezone("Europe/Copenhagen")
    )
    if now.hour == 7:
        return True
    return False


def is_in_previous_hour(email_datetime):
    """Check if datetime was in the previous hour."""
    now = datetime.now()
    previous_hour = (now - timedelta(hours=1)).replace(
        minute=0,
        second=0,
        microsecond=0
    )
    email_datetime_hour = email_datetime.replace(
        minute=0,
        second=0,
        microsecond=0
    )
    if previous_hour == email_datetime_hour:
        return True
    return False
