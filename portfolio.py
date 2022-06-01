from collections import defaultdict
from dataclasses import dataclass, field
import datetime
import numpy as np
from typing import List, Dict, Set, Optional
import pandas as pd
from pypfopt.discrete_allocation import DiscreteAllocation


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

    def __init__(self):

        self._allocations = dict()
        self._allocations_history = defaultdict(list)
        self._net_profit = 0.0

    def __len__(self):
        return len(self._allocations)

    def __hash__(self):
        return hash(str(self))

    def __str__(self) -> str:
        return "\n".join(
            str(allocation)
            for allocation in sorted(
                self._allocations.values(), key=lambda x: x.amount, reverse=True
            )
        )

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

    @property
    def allocations(self) -> Dict[str, Allocation]:
        """Get all allocations"""
        return self._allocations

    @property
    def net_profit(self) -> float:
        """Get net profit"""
        return self._net_profit

    def get_allocation(self, ticker: str) -> float:
        """Get allocation for a ticker"""
        return self._allocations[ticker]

    def get_allocation_tickers(self) -> List[str]:
        """Get tickers for allocations"""
        return list(self._allocations.keys())

    def get_total_allocation_amount(self) -> float:
        """Get total allocation"""
        return sum(allocation.amount for allocation in self._allocations.values())

    def add_allocation(
        self,
        tickers: List[str],
        weights: Dict[str, float],
        latest_prices: Dict[str, float],
        budget: float,
        verbose=True,
    ):
        """Set allocations"""
        assert len(tickers) == len(
            weights
        ), "Tickers and weights must be the same length"
        assert len(tickers) == len(
            latest_prices
        ), "Tickers and latest prices must be the same length"
        assert budget > 0, "Budget must be greater than 0"
        assert np.isclose(sum(weights.values()), 1), "Weights must sum to 1"

        da = DiscreteAllocation(
            weights, pd.Series(latest_prices), total_portfolio_value=budget
        )
        allocation, leftover = da.greedy_portfolio()
        if verbose:
            print("Discrete allocation:", allocation)
            print("Funds remaining: ${:.2f}".format(leftover))

        # Add new allocations
        for ticker in tickers:
            quantity = allocation.get(ticker, 0)
            amount = quantity * latest_prices[ticker]
            self._add_allocation(ticker, Allocation(ticker, quantity, amount))

    def get_current_portfolio_value(
        self, tickers, latest_prices: Dict[str, float]
    ) -> float:
        """Get current portfolio value"""
        return sum(
            allocation.quantity * latest_prices.get(ticker, 0)
            for ticker, allocation in self._allocations.items()
        )

    def get_portfolio_return(
        self,
        tickers,
        latest_prices: Dict[str, float],
        tags: Set[str] = None,
        verbose=True,
    ) -> float:
        """Get portfolio return"""
        if tags is not None:
            tickers = self.filter_tickers_using_tags(tags)
        if verbose:
            print("Tickers:", tickers)
        curr_portfolio_value = self.get_current_portfolio_value(tickers, latest_prices)
        amount_allocated = self.get_total_allocation_amount()
        return_pct = (
            (curr_portfolio_value - amount_allocated) / amount_allocated * 100.0
        )
        if verbose:
            print("Return: {:.2f}%".format(return_pct))
        return return_pct

    def filter_tickers_using_tags(self, tags: Set[str]) -> List[str]:
        """Filter allocations using tags"""
        return [
            ticker
            for ticker, allocation in self._allocations.items()
            if tags.intersection(allocation.tags)
        ]

    def save_to_storage(self, storage):
        """Save portfolio to storage"""
        # TODO: implement storage
        storage.set_portfolio(self)

    def load_from_storage(self, storage, hash=None):
        """Load portfolio from storage"""
        # TODO: implement storage
        portfolio = storage.get_portfolio(hash)
        self._allocations = portfolio._allocations
