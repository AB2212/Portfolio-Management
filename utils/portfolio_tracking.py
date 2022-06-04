from typing import Dict, List, Optional, Set

from portfolio import Portfolio


def filter_tickers_using_tags(portfolio: Portfolio, tags: Set[str]) -> List[str]:
    """Filter allocations using tags"""
    return [
        ticker
        for ticker, allocation in portfolio.allocations.items()
        if tags.intersection(allocation.tags)
    ]


def get_total_allocation_amount(portfolio: Portfolio) -> float:
    """Get total allocation"""
    return sum(allocation.amount for allocation in portfolio.allocations.values())


def get_current_portfolio_value(
    portfolio: Portfolio, latest_prices: Dict[str, float]
) -> float:
    """Get current portfolio value"""
    return sum(
        allocation.quantity * latest_prices[ticker]
        for ticker, allocation in portfolio.allocations.items()
    )


def get_portfolio_return(
    portfolio: Portfolio,
    tickers,
    latest_prices: Dict[str, float],
    tags: Set[str] = None,
    verbose=True,
) -> float:
    """Get portfolio return"""

    if tags is not None:
        tickers = filter_tickers_using_tags(portfolio, tags)
    if verbose:
        print("Tickers:", tickers)

    # Filter latest prices based on tags
    latest_prices = {k: v for k, v in latest_prices.items() if k in tickers}
    for ticker in tickers:
        if ticker not in latest_prices:
            raise ValueError(f"Ticker {ticker} not found")

    curr_portfolio_value = get_current_portfolio_value(portfolio, latest_prices)
    amount_allocated = get_total_allocation_amount(portfolio)
    return_pct = (curr_portfolio_value - amount_allocated) / amount_allocated * 100.0
    if verbose:
        print("Return: {:.2f}%".format(return_pct))
    return return_pct
