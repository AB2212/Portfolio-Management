import pandas as pd
import datetime

import requests_cache
import data_api

from typing import List, Tuple


class DataFetcher:
    """DataFetcher for asset prices"""

    def __init__(self, use_cache: bool = True, expire_after_days: int = 1) -> None:

        if use_cache:
            self._expire_after_days = datetime.timedelta(
                days=expire_after_days if expire_after_days > 0 else 1
            )
            self._cache_session = requests_cache.CachedSession(
                cache_name="cache",
                backend="sqlite",
                expire_after=self._expire_after_days,
            )
            self._cache_session.headers["User-agent"] = "my-program/1.0"
        else:
            self._expire_after_days = None
            self._cache_session = None

    def get_data_from_source(
        self,
        source: str,
        ticker: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> pd.DataFrame:
        """Get stock data from API"""
        if source == "yahoo":
            return data_api.get_data_from_yahoo(
                ticker, start_date, end_date, session=self._cache_session
            )
        elif source == "csv":
            return data_api.get_data_from_csv(ticker, start_date, end_date)
        elif source == "mfapi":
            return data_api.get_data_from_mfapi(
                ticker, start_date, end_date, session=self._cache_session
            )
        else:
            raise ValueError("Invalid source name")

    def _parse_ticker(self, ticker: str) -> Tuple[str]:
        """Parse ticker string"""
        if ":" in ticker:
            source, ticker = ticker.split(":")
        else:
            source = "yahoo"

        return source.strip(), ticker.strip()

    def get_data(
        self,
        tickers: List[str],
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> pd.DataFrame:

        if isinstance(tickers, str):
            tickers = [tickers]

        df = pd.DataFrame()
        for ticker in tickers:
            source, ticker = self._parse_ticker(ticker)
            df_ticker = self.get_data_from_source(source, ticker, start_date, end_date)
            df = df.join(df_ticker, how="outer")
        return df

    def get_latest_price(self, tickers: List[str]) -> pd.DataFrame:
        """Get latest price for all tickers"""
        if isinstance(tickers, str):
            tickers = [tickers]

        df = pd.DataFrame()
        for ticker in tickers:
            source, ticker = self._parse_ticker(ticker)
            df_ticker = self.get_data_from_source(
                source,
                ticker,
                datetime.datetime.now() - datetime.timedelta(days=7),
                datetime.datetime.now(),
            )
            df = df.join(df_ticker, how="outer")
        if df.empty:
            raise ValueError("No data found")
        df.fillna(method="ffill", inplace=True)
        latest_prices = df.iloc[-1].to_dict()
        return latest_prices


if __name__ == "__main__":

    data_fetcher = DataFetcher()
    df = data_fetcher.get_data(
        "GOOGL", datetime.datetime(2018, 1, 1), datetime.datetime(2018, 12, 31)
    )
    print(df)
    df = data_fetcher.get_data(
        ["GOOGL", "AMZN", "yahoo:AAPL", "mfapi:100357"],
        datetime.datetime(2018, 1, 1),
        datetime.datetime(2018, 12, 31),
    )
    print(df)
