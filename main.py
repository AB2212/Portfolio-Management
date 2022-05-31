from fetch_data import DataFetcher
from optimize import Optimize
from portfolio import Portfolio
import datetime
import matplotlib.pyplot as plt


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
    portfolio = Portfolio()
    latest_prices = fetcher.get_latest_price(tickers)
    portfolio.add_allocation(tickers, weights, latest_prices, budget, verbose)

    return portfolio


def main():
    """Main"""
    # Create portfolio
    portfolio = create_portfolio(
        ["GOOGL", "AAPL", "AMZN", "FB", "NFLX"],
        datetime.datetime(2004, 1, 1),
        datetime.datetime(2021, 12, 31),
        1000,
        verbose=True,
    )

    # Print portfolio
    print(portfolio)


if __name__ == "__main__":
    main()
