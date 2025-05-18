from stock_analysis.alphavantage_api.literals import StockSymbol

STOCK_SYMBOL_TO_NAME: dict[StockSymbol, str] = {
    "IBM": "International Business Machines Corporation",
    "DIS": "The Walt Disney Company",
    "CMCSA": "Comcast Corporation",
    "GME": "GameStop Corp.",
}


def get_stock_name(symbol: StockSymbol) -> str:
    return STOCK_SYMBOL_TO_NAME[symbol]
