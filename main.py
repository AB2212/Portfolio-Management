import datetime

import matplotlib.pyplot as plt

from fetch_data import DataFetcher
from optimize import Optimize
from portfolio import Portfolio


def create_portfolio(tickers, start_date, end_date, budget, *args, **kwargs):
    """Create portfolio"""
    verbose = kwargs.get("verbose", True)
    # Get data
    fetcher = DataFetcher()
    data = fetcher.get_data(tickers, start_date, end_date)

    # Optimize
    optimize = Optimize()
    weights = optimize.run(data)

    # Create portfolio
    portfolio = Portfolio("FAANG")
    latest_prices = fetcher.get_latest_price(tickers)
    portfolio.add_allocation(tickers, weights, latest_prices, budget, verbose)

    portfolio.save()

    return portfolio


def main():
    """Main"""
    # Create portfolio
    portfolio = create_portfolio(
        tickers=["GOOGL", "AAPL", "AMZN", "FB", "NFLX"],
        start_date=datetime.datetime(2010, 1, 1),
        end_date=datetime.datetime(2021, 12, 31),
        budget=1000,
        verbose=True,
    )

    # Print portfolio
    print(f"Portfolio: \n{portfolio}")


if __name__ == "__main__":
    main()
