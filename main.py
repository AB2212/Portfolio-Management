import datetime

from portfolio import create_portfolio


def main():
    """Main"""
    # Create portfolio
    portfolio = create_portfolio(
        portfolio_name="My FAANG portfolio",
        tickers=["FB", "AAPL", "AMZN", "NFLX", "GOOGL"],
        start_date=datetime.datetime(2010, 1, 1),
        end_date=datetime.datetime(2021, 12, 31),
        optimization_method="max_sharpe_ratio",
        allocation_strategy="discrete",
        budget=10000,
        verbose=True,
    )

    # Print portfolio
    print(f"Portfolio: \n{portfolio}")


if __name__ == "__main__":
    main()
