# Portfolio Optimization
One stop solution for managing and optimizing your portfolio

### Example code
    portfolio = create_portfolio(
            ["GOOGL", "AAPL", "AMZN", "FB", "NFLX"],
            datetime.datetime(2010, 1, 1),
            datetime.datetime(2021, 12, 31),
            budget=1000,
            verbose=True,
        )
    print(portfolio)

    ##### Output #####
    {'GOOGL': 0.0, 'AAPL': 0.49171, 'AMZN': 0.20015, 'FB': 0.12968, 'NFLX': 0.17846}
    Discrete allocation: {'AAPL': 3, 'NFLX': 1, 'FB': 1}
    Funds remaining: $153.09
    Allocation(ticker='AAPL', quantity=3, amount=450.6750183105469, tags=set())
    Allocation(ticker='NFLX', quantity=1, amount=198.91009521484375, tags=set())
    Allocation(ticker='FB', quantity=1, amount=197.32000732421875, tags=set())
    Allocation(ticker='GOOGL', quantity=0, amount=0.0, tags=set())
    Allocation(ticker='AMZN', quantity=0, amount=0.0, tags=set())
