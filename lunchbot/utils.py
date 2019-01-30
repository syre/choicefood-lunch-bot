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
    if (email_datetime.date() == previous_hour.date()) and (
            email_datetime.hour == previous_hour.hour):
        return True
    return False


def add_formatting(output):
    """Add some nice formatting to the message."""
    output = re.sub(r"\n{1,}", "\n\n", output)
    output = re.sub(r" {2}", "&nbsp;", output)
    return output


def remove_excessive_newlines(output):
    """Replace sequences of more than one newlines with just one."""
    output = re.sub(r"\n{1,}", "\n", output)
    return output


def convert_imap_date_to_datetime(date_str):
    """Convert imap date format 'Mon, 28 Jan 2019 08:14:23 +0000' to datetime."""
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")


def get_earliest_weekday_date(week_datetime):
    weekday = week_datetime.weekday()
    week_datetime -= timedelta(days=weekday)
    return week_datetime.replace(hour=0, minute=0, second=0)
