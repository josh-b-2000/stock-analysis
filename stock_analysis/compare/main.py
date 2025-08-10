import datetime as dt
import logging

import polars as pl
from matplotlib import pyplot as plt

from stock_analysis.alphavantage_api.constants import STOCK_SYMBOL_TO_COLOR
from stock_analysis.alphavantage_api.literals import AlphaVantageFunction, StockSymbol
from stock_analysis.alphavantage_api.utils import parse_cache_file_key
from stock_analysis.compare.utils import extract_cache_key, get_cached_files
from stock_analysis.extract.utils import STOCK_DATA_SCHEMA

logger = logging.getLogger()


def main() -> None:
    logger.info("Comparing all data in cache")

    cached_files = get_cached_files()

    if not cached_files:
        logger.error("No cached data found to compare")
        return

    logger.info("Data found for:")
    stock_data: dict[tuple[StockSymbol, AlphaVantageFunction], pl.DataFrame] = {}
    for file in cached_files:
        key = extract_cache_key(file)
        symbol, function, date_cached = parse_cache_file_key(key)
        logger.info(
            "    %s %s (cached %s)", symbol, function, date_cached.strftime("%m/%Y")
        )

        df = pl.read_csv(file, schema=STOCK_DATA_SCHEMA)

        df = df.with_columns(
            margin=pl.col("open") - pl.col("close"),
        ).with_columns(
            margin_normalised=pl.col("margin") / pl.col("margin").abs().max()
        )

        stock_data[(symbol, function)] = df

    _fig, ax = plt.subplots()

    for key, df in stock_data.items():
        symbol, function = key
        color = STOCK_SYMBOL_TO_COLOR[symbol]

        df = df.filter(df.get_column("date").gt(dt.date(2018, 1, 1)))

        date = df.get_column("date").to_list()
        margin_normalised = df.get_column("margin_normalised").to_list()

        ax.plot(date, margin_normalised, linewidth=1.0, color=color, label=symbol)

    ax.set_xlabel("Date")
    ax.set_ylabel("Change (Normalised)")
    ax.legend()

    plt.show()
