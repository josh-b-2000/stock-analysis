import datetime as dt
import logging
from typing import TypeGuard, cast, get_args
from urllib.parse import urlencode

import requests

from stock_analysis.alphavantage_api.literals import AlphaVantageFunction, StockSymbol
from stock_analysis.alphavantage_api.models import (
    AlphaVantageRequest,
    AlphaVantageResponse,
)
from stock_analysis.config import Settings

settings = Settings()
logger = logging.getLogger()

CACHE_FILE_KEY_DELIMITER = "__"


def is_valid_stock_symbol(maybe_symbol: str) -> TypeGuard[StockSymbol]:
    return maybe_symbol in get_args(StockSymbol)


def get_cache_file_key(symbol: StockSymbol, function: AlphaVantageFunction) -> str:
    today = dt.date.today().strftime("%Y_%m")
    return CACHE_FILE_KEY_DELIMITER.join([symbol, function, today]) + ".csv"


def parse_cache_file_key(key: str) -> tuple[StockSymbol, AlphaVantageFunction, dt.date]:
    symbol, function, date_cached = key.split(CACHE_FILE_KEY_DELIMITER)
    year, month = [int(value) for value in date_cached.split("_")]
    return (
        cast(StockSymbol, symbol),
        cast(AlphaVantageFunction, function),
        dt.date(year, month, day=1),
    )


def get_alphavantage_data(request: AlphaVantageRequest) -> AlphaVantageResponse:
    logger.info("Fetching data from alphavantage API")
    params = request.model_dump()
    query_string = urlencode({**params, "apikey": settings.alpha_vantage_api_key})

    url = f"{settings.alpha_vantage_base_url}?{query_string}"

    # Maybe implement a caching mechanism here to avoid spamming the API?
    response = requests.get(url)
    if not response.ok:
        raise Exception(
            f"Alphavantage API responded with code {response.status_code}, {response.json()}"
        )

    response_data = response.json()
    try:
        return AlphaVantageResponse.from_response(
            {**response_data, "function": request.function}
        )
    except Exception as e:
        logger.error("Failed to validate data: %o", response_data)
        raise e
