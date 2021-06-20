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


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup Market Data sensor")

    api_key = config.get(CONF_API_KEY).strip()
    cryptocurrency_name = config.get(CONF_CRYPTOCURRENCY_NAME).strip()
    #currency_name = config.get(CONF_CURRENCY_NAME).strip()
    update_frequency = timedelta(minutes=(int(config.get(CONF_UPDATE_FREQUENCY))))
    
    entities = []

    try:
        entities.append(
            MarketDataSensor(
                api_key, cryptocurrency_name, update_frequency
            )
        )
    except urllib.error.HTTPError as error:
        _LOGGER.error(error.reason)
        return False

    add_entities(entities)

class MarketDataSensor(Entity):
    def __init__(
        self, api_key, cryptocurrency_name, update_frequency
    ):
        self.api_key = api_key
        self.cryptocurrency_name = cryptocurrency_name
        #self.currency_name = currency_name
        self.update = Throttle(update_frequency)(self._update)
        #Inisialisasi Attribute yang akan ditampilkan
        self._name = SENSOR_PREFIX + "_" + cryptocurrency_name + "USD"
        self._symbol = None
        self._price = None
        self._logo = None
        self._state = None
        self._rank = None
        self._high = None
        self._high_time = None
        self._market_cap = None
        self._first_trade = None
        self._priceChange1H = None
        self._priceChange1D = None
        self._priceChange7D = None
        self._priceChange30D = None
        self._priceChangePct1H = None
        self._priceChangePct1D = None
        self._priceChangePct7D = None
        self._priceChangePct30D = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {ATTR_NAME: self._name, ATTR_SYMBOL: self._symbol, ATTR_PRICE: self._price, ATTR_LOGO: self._logo, ATTR_RANK: self._rank, ATTR_HIGH: self._high, ATTR_HIGH_TIME: self._high_time, ATTR_MARKET_CAP: self._market_cap, ATTR_FIRST_TRADE: self._first_trade, ATTR_TFH1: self._priceChange1H, ATTR_TF1D: self._priceChange1D, ATTR_TF7D: self._priceChange7D, ATTR_TF30D: self._priceChange30D, ATTR_TFH1PCT: self._priceChangePct1H, ATTR_TF1DPCT: self._priceChangePct1D, ATTR_TF7DPCT: self._priceChangePct7D, ATTR_TF30DPCT: self._priceChangePct30D}

    def _update(self):
        url = (
            API_ENDPOINT
            + "ticker?key="
            + self.api_key
            + "&ids="
            + self.cryptocurrency_name
            + "&interval=1h,1d,7d,30d"
            + "&per-page=100&page=1&sort=first_priced_at"
        )
        # sending get request
        r = requests.get(url=url)
        try:
            # Set the values of the sensor
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
            self._state = r.json()[0]["price"]
            # set the attributes of the sensor
            self._name = r.json()[0]["name"]
            self._symbol = r.json()[0]["symbol"]
            self._price = r.json()[0]["price"]
            self._logo = r.json()[0]["logo_url"]
            self._rank = r.json()[0]["rank"]
            self._high = r.json()[0]["high"]
            self._high_time = r.json()[0]["high_timestamp"]
            self._market_cap = r.json()[0]["market_cap"]
            self._first_trade = r.json()[0]["first_trade"]
            self._priceChange1H = r.json()[0]["1h"]["price_change"]
            self._priceChange1D = r.json()[0]["1d"]["price_change"]
            self._priceChange7D = r.json()[0]["7d"]["price_change"]
            self._priceChange30D = r.json()[0]["30d"]["price_change"]
            self._priceChangePct1H = r.json()[0]["1h"]["price_change_pct"]
            self._priceChangePct1D = r.json()[0]["1d"]["price_change_pct"]
            self._priceChangePct7D = r.json()[0]["7d"]["price_change_pct"]
            self._priceChangePct30D = r.json()[0]["30d"]["price_change_pct"]
        except ValueError:
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
            self._name = None
            self._symbol = None
            self._price = None
            self._logo = None
            self._rank = None
            self._high = None
            self._high_time = None
            self._market_cap = None
            self._first_trade = None
            self._priceChange1H = None
            self._priceChange1D = None
            self._priceChange7D = None
            self._priceChange30D = None
            self._priceChangePct1H = None
            self._priceChangePct1D = None
            self._priceChangePct7D = None
            self._priceChangePct30D = None