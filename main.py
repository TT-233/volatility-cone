import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from py_vollib.black_scholes.implied_volatility import implied_volatility

# 1. catch VIX data and calculate volatility cone
print("download VIX data...")
vix_data = yf.download('^VIX', start='2020-01-01', end='2024-01-01')
if vix_data.empty:
    print("Error: VIX data failed")
    exit()

windows = [21, 63, 126]  # define roll windows

# Calculate the annualized volatility for different rolling windows.
vix_volatilities = {}
for window in windows:
    rolling_vol = vix_data['Close'].rolling(window=window).std() * np.sqrt(252)
    vix_volatilities[window] = rolling_vol

# Combine the volatilities of different windows into a single DataFrame.
vix_volatility_df = pd.concat(vix_volatilities, axis=1).dropna()
vix_volatility_df.columns = [f'{window}-Day' for window in windows]
print(f"The rolling volatility calculation is complete, showing the first 5 rows of data.：\n{vix_volatility_df.head()}")

# Calculate the quantiles.
quantiles = {window: vix_volatility_df[f'{window}-Day'].quantile([0.1, 0.5, 0.9]) for window in windows}
print(f"Quantiles of the VIX volatility cone.：\n{quantiles}")

# Step2.Retrieve SPY (S&P 500 ETF) options data and calculate the implied volatility.
ticker = 'SPY'
stock = yf.Ticker(ticker)
print("check if the options data is available...")

# Check and select future option expiration dates.
future_expirations = [date for date in stock.options if pd.to_datetime(date) > pd.Timestamp.now()]

if not future_expirations:
    print("Error: No valid future option expiration dates are available.")
    exit()

# Retrieve the next available future option expiration date.
next_expiration = future_expirations[0]
print(f"The option expiration date being used: {next_expiration}")

# Retrieve the option chain.
options = stock.option_chain(next_expiration)
calls = options.calls

# Retrieve the current price of SPY.
current_price = stock.history(period="1d")['Close'].iloc[0]
print(f"SPY current price: {current_price}")

# Set the risk-free rate.
risk_free_rate = 0.05

# Transform  lastTradeDate as date form
calls['lastTradeDate'] = pd.to_datetime(calls['lastTradeDate'], errors='coerce')

# Define the current time and filter out expired option contracts.
today = pd.Timestamp.now().tz_localize('UTC')  # Ensure that today is timezone-aware.
calls = calls[calls['lastTradeDate'] > today]  # Filter out contracts with expiration dates that have already passed.
print("All expired contracts have been filtered out.")
print(f"The first 5 rows of valid options data.：\n{calls[['lastTradeDate', 'lastPrice', 'strike']].head()}")

# Use the apply function to calculate the ‘t’ value (time to expiration) for each row.
def calculate_time_to_expiration(date):
    if pd.notnull(date):
        delta = (date - today).days / 365  # Calculate the annualized value of the time to expiration.
        return delta
    return np.nan

# Calculate the value of ￼ (time to expiration) as the fraction of a year.
calls['t'] = calls['lastTradeDate'].apply(calculate_time_to_expiration)

# Calculate the implied volatility.
def calculate_implied_volatility(row):
    try:
        return implied_volatility(
            price=row['lastPrice'],
            S=current_price,
            K=row['strike'],
            t=row['t'],
            r=risk_free_rate,
            flag='c'
        )
    except Exception as e:
        print(f"Error calculating IV for row {row.name}: {e}")
        return np.nan

calls['implied_volatility'] = calls.apply(calculate_implied_volatility, axis=1)
print("The calculation of implied volatility is complete.")
print(f"Statistics on missing values for implied volatility.：\n{calls['implied_volatility'].isnull().sum()}")

# Calculate the quantiles of the implied volatility.
implied_quantiles = {
    '10%': calls['implied_volatility'].quantile(0.1),
    '50%': calls['implied_volatility'].quantile(0.5),
    '90%': calls['implied_volatility'].quantile(0.9),
}
print(f"SPY Implied volatility quantiles.：\n{implied_quantiles}")

# Step3. Plot the volatility cone and include the current implied volatility quantiles.
plt.figure(figsize=(12, 8))

# Plot the historical volatility cone for the VIX.
for window in windows:
    plt.plot(vix_volatility_df.index, vix_volatility_df[f'{window}-Day'], label=f'{window}-Day Rolling Volatility')

# Plot horizontal lines for VIX historical volatility quantiles.
colors = ['blue', 'orange', 'green']
for i, window in enumerate(windows):
    plt.axhline(quantiles[window].iloc[0], color=colors[i], linestyle='--', label=f"10% Quantile ({window}-Day)")
    plt.axhline(quantiles[window].iloc[1], color=colors[i], linestyle='-', label=f"50% Quantile ({window}-Day)")
    plt.axhline(quantiles[window].iloc[2], color=colors[i], linestyle='--', label=f"90% Quantile ({window}-Day)")

# If implied volatility data is available, plot its quantile lines.
plt.axhline(implied_quantiles['10%'], color='purple', linestyle='--', label='10% Implied Quantile (SPY)')
plt.axhline(implied_quantiles['50%'], color='purple', linestyle='-', label='50% Implied Quantile (SPY)')
plt.axhline(implied_quantiles['90%'], color='purple', linestyle='--', label='90% Implied Quantile (SPY)')

# Graph setting
plt.title('VIX Volatility Cone with SPY Implied Volatility')
plt.xlabel('Date')
plt.ylabel('Annualized Volatility')
plt.legend()
plt.show()