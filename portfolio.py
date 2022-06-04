import datetime
import os
import sys
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
from pypfopt.discrete_allocation import DiscreteAllocation

import utils.storage as storage
from fetch_data import DataFetcher
from optimize import OptimizePortfolio


@dataclass(frozen=True)
class Allocation:
    ticker: str
    quantity: float
    amount: float
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    tags: Optional[Set[str]] = field(default_factory=set)

    def __add__(self, other: "Allocation"):
        assert self.ticker == other.ticker, "Ticker must be the same"
        return Allocation(
            self.ticker, self.quantity + other.quantity, self.amount + other.amount
        )

    def __sub__(self, other: "Allocation"):
        assert self.ticker == other.ticker, "Ticker must be the same"
        return Allocation(
            self.ticker, self.quantity - other.quantity, self.amount - other.amount
        )

    def __mul__(self, other):

        if isinstance(other, int) or isinstance(other, float):

            return Allocation(
                self.ticker,
                self.quantity * other,
                self.amount * other,
                datetime.datetime.now(),
                self.tags,
            )
        else:
            raise TypeError("Multiplication not supported")


class Portfolio:
    """Maintains the portfolio details"""

    def __init__(self, portfolio_name: str):
        """Initialize portfolio"""
        self._portfolio_name = portfolio_name
        self._allocations = dict()
        self._allocations_history = defaultdict(list)
        self._net_profit = 0.0

    @property
    def allocations(self) -> Dict[str, Allocation]:
        """Get all allocations"""
        return self._allocations

    @property
    def net_profit(self) -> float:
        """Get net profit"""
        return self._net_profit

    @property
    def portfolio_name(self) -> str:
        return self._portfolio_name

    def _add_allocation(self, ticker: str, allocation: Allocation):
        """Add allocation for a ticker"""
        self._allocations_history[ticker].append(allocation)
        if ticker in self._allocations:
            self._allocations[ticker] += allocation
        else:
            self._allocations[ticker] = allocation

    def _sub_allocation(self, ticker: str, allocation: Allocation):
        """Subtract allocation for a ticker"""
        curr_amount = 0
        self._allocations_history[ticker].append(allocation)
        if ticker in self._allocations:
            curr_amount = self._allocations[ticker].amount
            self._allocations[ticker] -= allocation
        else:
            # Short position
            self._allocations[ticker] = -allocation

        self._net_profit += allocation.amount - curr_amount

    def _delete_allocation(self, ticker: str):
        """Delete allocation for a ticker"""
        del self._allocations[ticker]
        del self._allocations_history[ticker]

    def add_allocation(
        self,
        allocations: List[Allocation],
    ):
        # Add new allocations
        for allocation in allocations:
            self._add_allocation(allocation.ticker, allocation)

    def _update_id_history(self, id, dirname):
        """Update id history"""
        id_history_filepath = os.path.join(dirname, "id_history.pkl")
        if os.path.exists(id_history_filepath):
            hash_history = storage.load_object(id_history_filepath)
            hash_history.append(id)
            storage.save_object(hash_history, id_history_filepath)
        else:
            hash_history = [id]
            storage.save_object(hash_history, id_history_filepath)

    def save(self):
        """Save portfolio"""
        dirname = f"./portfolios/{self.portfolio_name}"
        os.makedirs(dirname, exist_ok=True)
        id = hash(self)
        storage.save_object(self, os.path.join(dirname, f"{id}.pkl"))
        self._update_id_history(id, dirname)

    def load(self, id=None):
        """Load portfolio"""
        dirname = f"./portfolios/{self.portfolio_name}"
        id_history_filepath = os.path.join("./portfolios/", "id_history.pkl")
        if id is None and os.path.exists(id_history_filepath):
            # Loading latest id
            ids = storage.load_object(id_history_filepath)
            if not ids:
                raise ValueError("No portfolios found")
            id = ids[-1]
        filepath = os.path.join(dirname, f"{id}.pkl")
        if not os.path.exists(filepath):
            raise ValueError(f"Portfolio with id {id} not found")
        return storage.load_object(filepath)

    def __len__(self):
        return len(self._allocations)

    def __hash__(self):
        return hash(str(self)) % ((sys.maxsize + 1) * 2)  # Ensures postive hash value

    def __str__(self) -> str:
        return "\n".join(
            str(allocation)
            for allocation in sorted(
                self._allocations.values(), key=lambda x: x.amount, reverse=True
            )
        )


def allocate(
    allocation_strategy: str,
    weights: Dict[str, float],
    latest_prices: Dict[str, float],
    budget: float,
) -> Tuple[Dict[str, float], float]:
    """Allocate portfolio weights"""
    # TODO: add more allocation strategies
    if allocation_strategy == "discrete":
        da = DiscreteAllocation(
            weights, pd.Series(latest_prices), total_portfolio_value=budget
        )
        allocation, leftover = da.greedy_portfolio()
    else:
        raise ValueError(f"Unknown allocation method {allocation_strategy}")

    return allocation, leftover


def create_allocations(
    weights: Dict[str, float],
    latest_prices: Dict[str, float],
    budget: float,
    allocation_strategy="discrete",
    verbose=True,
):
    """Set allocations"""
    assert set(weights) == set(
        latest_prices
    ), "Tickers must be the same for weights and latest_prices"
    assert budget > 0, "Budget must be greater than 0"
    assert np.isclose(sum(weights.values()), 1), "Weights must sum to 1"

    allocation, left_over = allocate(
        allocation_strategy, weights, latest_prices, budget
    )
    if verbose:
        print("Discrete allocation:", allocation)
        print("Funds remaining: ${:.2f}".format(left_over))

    # Add new allocations
    allocations = []
    for ticker, latest_price in latest_prices.items():
        quantity = allocation.get(ticker, 0)
        amount = quantity * latest_price
        allocations.append(Allocation(ticker, quantity, amount))

    return allocations


def create_portfolio(
    portfolio_name: str,
    tickers: Union[str, List[str]],
    start_date,
    end_date,
    optimization_method,
    allocation_strategy,
    budget,
    *args,
    **kwargs,
):
    """Create portfolio"""

    if isinstance(tickers, str):
        tickers = [tickers]
    verbose = kwargs.get("verbose", True)
    # Get data
    fetcher = DataFetcher()
    data = fetcher.get_data(tickers, start_date, end_date)

    # Optimize
    optimize = OptimizePortfolio(optimization_method)
    weights = optimize.run(data)

    # Create allocations
    latest_prices = fetcher.get_latest_price(tickers)
    allocations = create_allocations(
        weights, latest_prices, budget, allocation_strategy, verbose
    )

    # Create portfolio
    portfolio = Portfolio(portfolio_name)
    portfolio.add_allocation(allocations)

    portfolio.save()

    return portfolio
