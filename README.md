# Portfolio Management
One stop solution for managing and optimizing your portfolio

### Example

```python
import datetime
from portfolio import create_portfolio

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

print(f"Portfolio: \n{portfolio}")
```
    Allocation Proportion: {'FB': 0.12968, 'AAPL': 0.49171, 'AMZN': 0.20015, 'NFLX': 0.17846, 'GOOGL': 0.0}
    Discrete allocation: {'AAPL': 33, 'AMZN': 1, 'NFLX': 8, 'FB': 6}
    Funds remaining: $18.94
    Portfolio:
    Allocation(ticker='AAPL', quantity=33, amount=4797.5401611328125, timestamp=datetime.datetime(2022, 6, 4, 11, 8, 14, 485409), tags=set())
    Allocation(ticker='AMZN', quantity=1, amount=2447.0, timestamp=datetime.datetime(2022, 6, 4, 11, 8, 14, 485409), tags=set())
    Allocation(ticker='NFLX', quantity=8, amount=1591.8399658203125, timestamp=datetime.datetime(2022, 6, 4, 11, 8, 14, 485409), tags=set())
    Allocation(ticker='FB', quantity=6, amount=1144.6799926757812, timestamp=datetime.datetime(2022, 6, 4, 11, 8, 14, 485409), tags=set())
    Allocation(ticker='GOOGL', quantity=0, amount=0.0, timestamp=datetime.datetime(2022, 6, 4, 11, 8, 14, 485409), tags=set())
