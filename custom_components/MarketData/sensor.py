#!/usr/bin/env python3
"""
URL Market Data API
https://api.nomics.com/v1/currencies/ticker?key=your-key-here&ids=BTC,ETH,XRP&interval=1d,30d&convert=EUR&per-page=100&page=1
https://api.nomics.com/v1/currencies/ticker?key=kunci-nya&ids=pair&interval=time-Frame&per-page=100&page=1&sort=first_priced_at
"""

import requests
import voluptuous as vol
from datetime import datetime, date, timedelta
import urllib.error

from .const import (
    _LOGGER,
    CONF_ID,
    CONF_API_KEY,
    CONF_CRYPTOCURRENCY_NAME,
    #CONF_CURRENCY_NAME,
    CONF_UPDATE_FREQUENCY,
    SENSOR_PREFIX,
    ATTR_NAME,
    ATTR_SYMBOL,
    ATTR_PRICE,
    ATTR_LOGO,
    ATTR_RANK,
    ATTR_HIGH,
    ATTR_HIGH_TIME,
    ATTR_MARKET_CAP,
    ATTR_FIRST_TRADE,
    ATTR_TFH1,
    ATTR_TF1D,
    ATTR_TF7D,
    ATTR_TF30D,
    ATTR_TFH1PCT,
    ATTR_TF1DPCT,
    ATTR_TF7DPCT,
    ATTR_TF30DPCT,
    API_ENDPOINT,
)

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend( #Set nilai default config
    {
        vol.Required(CONF_CRYPTOCURRENCY_NAME, default="BTC"): cv.string,
        #vol.Required(CONF_CURRENCY_NAME, default="USD"): cv.string,
        vol.Required(CONF_UPDATE_FREQUENCY, default=60): cv.string,
        vol.Required(CONF_API_KEY, default="683a2cef97864abf98068dd9e074c9010a61c2ac"): cv.string,
        vol.Optional(CONF_ID, default = ""): cv.string,
    }
)