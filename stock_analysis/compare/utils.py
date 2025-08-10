import glob
from pathlib import Path

from stock_analysis.constants import ALPHAVANTAGE_CACHE_DIR


def get_cached_files() -> list[str]:
    return glob.glob(str(Path(ALPHAVANTAGE_CACHE_DIR).joinpath("*.csv")))


def extract_cache_key(cache_file: str) -> str:
    prefix = ALPHAVANTAGE_CACHE_DIR + "/"
    suffix = ".csv"
    return cache_file.removeprefix(prefix).removesuffix(suffix)
