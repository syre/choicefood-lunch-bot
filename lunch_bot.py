#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from microsoftbotframework import MsBot
from tasks import *


bot = MsBot()
bot.add_process(fetch_lunch_response)
bot.add_process(rate_lunch_response)

if __name__ == '__main__':
	bot.run()