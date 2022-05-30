import pandas as pd
import pandas_datareader.data as web
import datetime
import requests


def get_data_from_yahoo(
    ticker: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    session=None,
) -> pd.DataFrame:
    """Get stock data from Yahoo Finance"""
    df = web.DataReader(ticker, "yahoo", start_date, end_date, session=session)
    df = df[["Adj Close"]]
    df.rename(columns={"Adj Close": ticker}, inplace=True)
    return df


def get_data_from_mfapi(
    ticker: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    session=None,
) -> pd.DataFrame:
    """Get stock data from mfapi"""
    url = f"https://api.mfapi.in/mf/{ticker}"
    if session is not None:
        response = session.get(url)
    else:
        response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error getting data from {url}")
    data = response.json()
    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"])
    df["nav"] = df["nav"].astype(float)
    df.rename(columns={"nav": ticker}, inplace=True)
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df.set_index("date", inplace=True)
    return df


def get_data_from_csv(ticker, start_date, end_date):
    """Get stock data from CSV file"""
    df = pd.read_csv(ticker + ".csv", index_col=0, parse_dates=True)
    return df.loc[start_date:end_date]
