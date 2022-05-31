# Portfolio Optimization
One stop solution for managing and optimizing your portfolio

### Example

```python
portfolio = create_portfolio(
    tickers=["GOOGL", "AAPL", "AMZN", "FB", "NFLX"],
    start_date=datetime.datetime(2010, 1, 1),
    end_date=datetime.datetime(2021, 12, 31),
    budget=1000,
    verbose=True,
)

print(f"Portfolio: \n{portfolio}")
```
    Allocation Proportion: {'GOOGL': 0.0, 'AAPL': 0.49171, 'AMZN': 0.20015, 'FB': 0.12968, 'NFLX': 0.17846}
    Discrete allocation: {'AAPL': 3, 'NFLX': 1, 'FB': 1}
    Funds remaining: $155.07
    Portfolio:
    Allocation(ticker='AAPL', quantity=3, amount=449.8140106201172, tags=set())
    Allocation(ticker='NFLX', quantity=1, amount=198.06500244140625, tags=set())
    Allocation(ticker='FB', quantity=1, amount=197.05279541015625, tags=set())
    Allocation(ticker='GOOGL', quantity=0, amount=0.0, tags=set())
    Allocation(ticker='AMZN', quantity=0, amount=0.0, tags=set())
