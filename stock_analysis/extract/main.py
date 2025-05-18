import logging

import matplotlib.pyplot as plt

from stock_analysis.alphavantage_api.constants import get_stock_name
from stock_analysis.alphavantage_api.literals import StockSymbol
from stock_analysis.alphavantage_api.models import AlphaVantageRequest
from stock_analysis.alphavantage_api.utils import get_alphavantage_data
from stock_analysis.extract.utils import get_cache_data, update_cache

logger = logging.getLogger()


def main(symbol: StockSymbol) -> None:
    stock_name = get_stock_name(symbol)
    logger.info(f"Extracting stock data for '{stock_name} ({symbol})'")

    request = AlphaVantageRequest(
        function="TIME_SERIES_WEEKLY", symbol=symbol, data_type="json"
    )

    logger.info("Attempting to read from cache")
    cache_data = get_cache_data(request)
    if cache_data is None:
        api_data = get_alphavantage_data(request)
        cache_data = update_cache(request, api_data)

    date = cache_data.get_column("date").to_list()
    open = cache_data.get_column("open").to_list()
    close = cache_data.get_column("close").to_list()

    _fig, ax = plt.subplots()

    ax.plot(date, open, linewidth=1.0, color="r")
    ax.plot(date, close, linewidth=1.0, color="b")

    plt.show()
