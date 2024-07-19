import numpy as np
import pandas as pd
from config import split_date, momentum_weights, file_path, column_names, bounds, constraints
from data_processing import load_data
from optimization import mean_variance_optimization, optimize_portfolio, calculate_momentum, get_adjusted_expected_returns
from performance import performance_metrics

np.random.seed(20)

fn_data = load_data(file_path, column_names)
returns = fn_data.pct_change().dropna()

in_sample_returns = returns[returns.index < split_date]
out_sample_returns = returns[returns.index >= split_date]

cov_matrix = returns.cov() * 252

# Define current weights (previous allocation to account for transaction cost) 
current_weights = [
    0.0178,      # KOSPI
    0.12857,  # KOSDAQ
    0.20066,   # S&P 500
    0.0,      # STOXX 50
    0.19646,  # Nikkei 225
    0.0,      # CSI 300
    0.0,      # 국채 10년
    0.0,      # 우량회사채
    0.20219,  # 해외채권
    0.12687,   # 금
    0.07512,  # WTI
    0.0,      # KOSPI Short
    0.05827,  # US Long
    0.0,      # US Short
    0.0,      # MMF
]

results = []

for momentum_weight in momentum_weights:
    momentum_factor = calculate_momentum(fn_data)
    adjusted_expected_returns = get_adjusted_expected_returns(returns, momentum_factor, momentum_weight)

    n_assets = len(returns.columns)
    initial_weights = np.random.dirichlet(np.ones(n_assets), size=1)[0]

    result = optimize_portfolio(initial_weights, adjusted_expected_returns, cov_matrix, current_weights, bounds, constraints)

    if result.success:
        optimized_weights = result.x
        out_sample_portfolio_returns = np.dot(out_sample_returns, optimized_weights)
        out_sample_portfolio_returns = pd.Series(out_sample_portfolio_returns, index=out_sample_returns.index)
        metrics = performance_metrics(out_sample_portfolio_returns)
        results.append([momentum_weight] + list(optimized_weights * 100) + [metrics[1] * 100, metrics[2] * 100])
    else:
        results.append([momentum_weight] + [np.nan] * n_assets + [np.nan, np.nan])

column_names_extended = ["Momentum"] + column_names[1:] + ["Annual Return", "Annual Volatility"]
mvo_momentum_df = pd.DataFrame(results, columns=column_names_extended)

mmf_index = mvo_momentum_df.columns.get_loc("MMF") + 1
mvo_momentum_df.insert(mmf_index, "Cash", 1.0)

print(mvo_momentum_df.round(2))

mvo_momentum_df.round(2).to_csv("mvo_momentum_df.csv", encoding="UTF-8-SIG")
