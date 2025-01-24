import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf  # Library to fetch stock data

# Fetch NVIDIA stock data
ticker = "NVDA"
stock_data = yf.download(ticker, period="5y", interval="1d")  # Download 5 years of daily data

# Calculate historical volatility (annualized)
daily_returns = stock_data['Adj Close'].pct_change().dropna()
historical_volatility = daily_returns.std() * np.sqrt(252)  # Annualize volatility

# NVIDIA fundamental parameters (as of October 2023)
pe_ratio = 110.0  # Price-to-Earnings ratio
dividend_yield = 0.0003  # Dividend yield (0.03%)
earnings_growth_rate = 0.20  # Expected earnings growth rate (20%)

# Investment parameters
initial_investment = 100000  # Initial investment amount
years = 10  # Investment horizon in years
num_simulations = 1000  # Number of Monte Carlo simulations

# Calculate expected annual return using fundamental values
# Expected return = Earnings Growth Rate + Dividend Yield
expected_annual_return = earnings_growth_rate + dividend_yield

# Function to simulate portfolio value using Monte Carlo
def monte_carlo_simulation(initial_investment, expected_annual_return, historical_volatility, years, num_simulations):
    results = np.zeros((years + 1, num_simulations))
    results[0] = initial_investment

    for i in range(1, years + 1):
        # Generate random returns based on expected return and volatility
        random_returns = np.random.normal(expected_annual_return / 252, historical_volatility / np.sqrt(252), num_simulations)
        # Update portfolio value
        results[i] = results[i - 1] * (1 + random_returns)

    return results

# Run the simulation
simulation_results = monte_carlo_simulation(initial_investment, expected_annual_return, historical_volatility, years, num_simulations)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(simulation_results)
plt.title(f'Monte Carlo Simulation of NVIDIA ({ticker}) Portfolio Value')
plt.xlabel('Years')
plt.ylabel('Portfolio Value ($)')
plt.show()

# Analyze the results
final_values = simulation_results[-1]
mean_final_value = np.mean(final_values)
median_final_value = np.median(final_values)
percentile_5 = np.percentile(final_values, 5)
percentile_95 = np.percentile(final_values, 95)

print(f"Mean final portfolio value: ${mean_final_value:,.2f}")
print(f"Median final portfolio value: ${median_final_value:,.2f}")
print(f"5th percentile final portfolio value: ${percentile_5:,.2f}")
print(f"95th percentile final portfolio value: ${percentile_95:,.2f}")

# Provide investment advice
if mean_final_value > initial_investment:
    print("Based on the simulation, the investment in NVIDIA is expected to grow.")
else:
    print("Based on the simulation, the investment in NVIDIA is expected to decline.")

if percentile_5 > initial_investment:
    print("Even in the worst-case scenario (5th percentile), the investment is expected to grow.")
else:
    print("In the worst-case scenario (5th percentile), the investment may decline.")
