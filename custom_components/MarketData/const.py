#DOMAIN = "MarketData"
import logging

CONF_ID = "id"
CONF_API_KEY = "api_key"
CONF_CRYPTOCURRENCY_NAME = "cryptocurrency_name"
#CONF_CURRENCY_NAME = "currency_name"
CONF_UPDATE_FREQUENCY = "update_frequency"

SENSOR_PREFIX = "MarketData"
ATTR_NAME= "name"
ATTR_SYMBOL = "symbol"
ATTR_PRICE = "price"
ATTR_LOGO = "logo_url"
ATTR_RANK = "rank"
ATTR_HIGH = "high"
ATTR_HIGH_TIME = "high_timestamp"
ATTR_MARKET_CAP = "market_cap"
ATTR_FIRST_TRADE = "first_trade"
ATTR_TFH1 = "price_change_h1"
ATTR_TF1D = "price_change_1d"
ATTR_TF7D = "price_change_7d"
ATTR_TF30D = "price_change_30d"
ATTR_TFH1PCT = "price_change_pct_h1"
ATTR_TF1DPCT = "price_change_pct_1d"
ATTR_TF7DPCT = "price_change_pct_7d"
ATTR_TF30DPCT = "price_change_pct_30d"

API_ENDPOINT = "https://api.nomics.com/v1/currencies/"

_LOGGER = logging.getLogger(__name__)