import logging

import typer

from stock_analysis.alphavantage_api.utils import is_valid_stock_symbol
from stock_analysis.extract.main import main as extract_main

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s (%(asctime)s): %(message)s",
    datefmt="%H:%M:%S",
)
app = typer.Typer()


@app.command()
def extract(stock_symbol: str) -> None:
    if not is_valid_stock_symbol(stock_symbol):
        raise ValueError(f"Invalid stock symbol '{stock_symbol}'")

    extract_main(stock_symbol)


@app.command()
def recommend_buy() -> None:
    raise NotImplementedError()


def cli() -> None:
    app()


if __name__ == "__main__":
    cli()
