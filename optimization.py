import numpy as np
from scipy.optimize import minimize
from config import transaction_cost 

def mean_variance_optimization(
    weights, expected_returns, cov_matrix, current_weights, risk_aversion=1
):
    portfolio_return = np.dot(weights, expected_returns)
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    utility = -portfolio_return + risk_aversion * portfolio_variance

    transaction_costs = np.sum(np.abs(weights - current_weights)) * transaction_cost

    adjusted_utility = utility + transaction_costs

    return adjusted_utility


def optimize_portfolio(
    initial_weights, expected_returns, cov_matrix, current_weights, bounds, constraints
):
    result = minimize(
        mean_variance_optimization,
        initial_weights,
        args=(expected_returns, cov_matrix, current_weights, 1),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    return result


def calculate_momentum(fn_data):
    momentum = (fn_data.pct_change(252) - fn_data.pct_change(21)).dropna()
    return momentum.mean()


def get_adjusted_expected_returns(returns, momentum_factor, momentum_weight):
    expected_returns = returns.mean() * 252
    return (1 - momentum_weight) * expected_returns + momentum_weight * momentum_factor
