import logging
from pathlib import Path

import polars as pl

from stock_analysis.alphavantage_api.models import (
    AlphaVantageRequest,
    AlphaVantageResponse,
)
from stock_analysis.alphavantage_api.utils import get_cache_file_key
from stock_analysis.constants import ALPHAVANTAGE_CACHE_DIR

logger = logging.getLogger()

STOCK_DATA_SCHEMA = {
    "symbol": pl.Utf8,
    "date": pl.Date,
    "open": pl.Float64,
    "high": pl.Float64,
    "low": pl.Float64,
    "close": pl.Float64,
    "volume": pl.Float64,
}


def create_stock_df(response: AlphaVantageResponse) -> pl.DataFrame:
    return pl.from_dicts(
        [
            {**stock_data.model_dump(), "symbol": response.meta_data.symbol}
            for stock_data in response.weekly_time_series
        ],
        schema=STOCK_DATA_SCHEMA,
        strict=True,
    ).sort(by="date")


def update_cache(
    request: AlphaVantageRequest, response: AlphaVantageResponse
) -> pl.DataFrame:
    file_key = get_cache_file_key(response.meta_data.symbol, request.function)
    df = create_stock_df(response)

    # Move this to some common function which always runs - some kind of set up
    base_path = Path(ALPHAVANTAGE_CACHE_DIR)
    base_path.mkdir(exist_ok=True)

    df.write_csv(base_path.joinpath(file_key))
    return df


def get_cache_data(request: AlphaVantageRequest) -> pl.DataFrame | None:
    file_key = get_cache_file_key(request.symbol, request.function)
    try:
        df = pl.read_csv(
            Path(ALPHAVANTAGE_CACHE_DIR).joinpath(file_key), schema=STOCK_DATA_SCHEMA
        )
        logger.info("Cache data found")
        return df
    except FileNotFoundError:
        logger.info("Could not find data in cache")
        return None
