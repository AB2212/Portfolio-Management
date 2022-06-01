# Portfolio Management
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
Funds remaining: $162.40
Portfolio:
Allocation(ticker='AAPL', quantity=3, amount=446.5199890136719, timestamp=datetime.datetime(2022, 6, 1, 13, 43, 14, 605292), tags=set())
Allocation(ticker='NFLX', quantity=1, amount=197.44000244140625, timestamp=datetime.datetime(2022, 6, 1, 13, 43, 14, 605292), tags=set())
Allocation(ticker='FB', quantity=1, amount=193.63999938964844, timestamp=datetime.datetime(2022, 6, 1, 13, 43, 14, 605292), tags=set())
Allocation(ticker='GOOGL', quantity=0, amount=0.0, timestamp=datetime.datetime(2022, 6, 1, 13, 43, 14, 605292), tags=set())
Allocation(ticker='AMZN', quantity=0, amount=0.0, timestamp=datetime.datetime(2022, 6, 1, 13, 43, 14, 605292), tags=set())
