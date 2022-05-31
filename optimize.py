import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage


class Optimize:
    """Optimize portfolio"""

    # TODO: Add more methods
    def __init__(self, method=None, verbose=True):

        self.method = method
        self.verbose = verbose

    def _max_sharpe_ratio(self, data: pd.DataFrame):
        """Max Sharpe Ratio"""
        mu = mean_historical_return(data)
        S = CovarianceShrinkage(data).ledoit_wolf()
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        cleaned_weights = dict(ef.clean_weights())
        if self.verbose:
            print(f"Allocation Proportion: {cleaned_weights}")
        return cleaned_weights

    def run(self, data):
        """Run"""
        return self._max_sharpe_ratio(data)
