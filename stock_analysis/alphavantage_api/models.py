import datetime as dt
from typing import Any, Self

from pydantic import BaseModel, model_validator

from stock_analysis.alphavantage_api.literals import (
    AlphaVantageFunction,
    DataType,
    StockSymbol,
)


class AlphaVantageRequest(BaseModel):
    function: AlphaVantageFunction
    symbol: StockSymbol
    data_type: DataType


class MetaData(BaseModel):
    information: str
    symbol: StockSymbol
    last_refreshed: dt.date
    time_zone: str

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Self:
        return cls(
            information=data["1. Information"],
            symbol=data["2. Symbol"],
            last_refreshed=dt.date.fromisoformat(data["3. Last Refreshed"]),
            time_zone=data["4. Time Zone"],
        )


class StockData(BaseModel):
    date: dt.date
    open: float
    high: float
    low: float
    close: float
    volume: float

    @classmethod
    def from_response(cls, key: str, item: dict[str, str]) -> Self:
        return cls(
            date=dt.date.fromisoformat(key),
            open=float(item["1. open"]),
            high=float(item["2. high"]),
            low=float(item["3. low"]),
            close=float(item["4. close"]),
            volume=float(item["5. volume"]),
        )


class AlphaVantageResponse(BaseModel):
    meta_data: MetaData
    weekly_time_series: list[StockData]

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Self:
        return cls(
            meta_data=MetaData.from_response(data["Meta Data"]),
            weekly_time_series=[
                StockData.from_response(key, item)
                for key, item in data["Weekly Time Series"].items()
            ],
        )

    @model_validator(mode="after")
    def sort_time_series(self) -> Self:
        self.weekly_time_series.sort(key=lambda item: item.date)
        return self
