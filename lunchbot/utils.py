#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module containing various utilities for the lunch bot.
"""
import re
from datetime import (
    datetime,
    timedelta,
)
from pytz import timezone

def is_seven_o_clock_danish_time(datetime):
    """Check if datetime is in seven o clock range in Denmark."""
    danish_timezone = timezone("Europe/Copenhagen")
    danish_time = datetime.astimezone(danish_timezone)

    if danish_time.hour == 7:
        return True
    return False


def is_in_previous_hour(now_datetime, email_datetime):
    """Check if datetime was in the previous hour compared to now."""
    previous_hour = (now_datetime - timedelta(hours=1))
    if email_datetime.hour == previous_hour.hour:
        return True
    return False

def add_formatting(output):
    """Add some nice formatting to the message"""
    output = re.sub(r"\n{1,}", "\n\n", output)
    output = re.sub(r" {2}", "&nbsp;", output)
    return output

def remove_excessive_newlines(output):
    """Replace sequences of more than one newlines with just one"""
    output = re.sub(r"\n{1,}", "\n", output)
    return output
