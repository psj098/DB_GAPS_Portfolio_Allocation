import numpy as np

def performance_metrics(returns):
    cumulative_return = (returns + 1).prod() - 1
    annualized_return = returns.mean() * 252
    annualized_volatility = returns.std() * np.sqrt(252)
    return cumulative_return, annualized_return, annualized_volatility
