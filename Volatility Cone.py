import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Fetch VIX and SPY data
vix_data = yf.download('^VIX', start='2010-01-01', end='2024-01-01')
spy_data = yf.download('SPY', start='2010-01-01', end='2024-01-01')

# Ensure indexes are datetime
spy_data.index = pd.to_datetime(spy_data.index)
vix_data.index = pd.to_datetime(vix_data.index)

# Calculate SPY daily returns and clean NaN values
spy_data['returns'] = spy_data['Adj Close'].pct_change()
spy_data = spy_data.dropna()  # Remove NaN rows

# Define rolling window sizes
windows = [21, 42, 63, 126, 189]
rolling_stats = {}
realized_volatility = {}

# Step 2: Calculate rolling statistics
for window in windows:
    # Implied Volatility (VIX rolling statistics)
    rolling_volatility = vix_data['Close'].rolling(window).std() * np.sqrt(252)
    rolling_stats[window] = {
        'Max': rolling_volatility.max(),
        '75th Percentile': rolling_volatility.quantile(0.75),
        'Mean': rolling_volatility.mean(),
        '25th Percentile': rolling_volatility.quantile(0.25),
        'Min': rolling_volatility.min(),
    }
    # Realized Volatility (SPY rolling statistics)
    realized_volatility[window] = spy_data['returns'].rolling(window).std().mean() * np.sqrt(252)

# Convert statistics into DataFrame
stats_df = pd.DataFrame({
    window: {
        "Max": rolling_stats[window]['Max'],
        "75th Percentile": rolling_stats[window]['75th Percentile'],
        "Mean": rolling_stats[window]['Mean'],
        "25th Percentile": rolling_stats[window]['25th Percentile'],
        "Min": rolling_stats[window]['Min'],
    } for window in windows
}).T

# Step 3: Plot implied and realized volatility in one figure
fig, ax1 = plt.subplots(figsize=(12, 8))

# Implied Volatility (solid lines)
y_columns = ['Max', '75th Percentile', 'Mean', '25th Percentile', 'Min']
colors = ['blue', 'orange', 'green', 'red', 'purple']

for i, col in enumerate(y_columns):
    y = stats_df[col].values
    ax1.plot(windows, y, label=f"Implied {col}", color=colors[i], marker='o')  # Original points

ax1.set_xlabel("Rolling Window Size (Days)", fontsize=12)
ax1.set_ylabel("Annualized Implied Volatility (%)", fontsize=12)
ax1.set_title("Volatility Cone: Implied vs Realized", fontsize=16)
ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# Add Realized Volatility (dashed lines)
ax2 = ax1.twinx()

# Dynamically adjust Realized Volatility axis range
realized_min = min(realized_volatility.values()) * 100
realized_max = max(realized_volatility.values()) * 100
ax2.set_ylim(realized_min - 1, realized_max + 1)  # Add padding for clarity

line_styles = ['--', '-.', ':', '--', '-.']  # Different dashed styles
for i, window in enumerate(windows):
    ax2.axhline(realized_volatility[window] * 100, linestyle=line_styles[i], color=colors[i],
                alpha=0.7, linewidth=1.5, label=f"Realized Vol ({window}-Day)")

ax2.set_ylabel("Realized Volatility (%)", fontsize=12)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# Automatically adjust legend location to avoid overlap
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper center", bbox_to_anchor=(0.5, -0.1), fontsize=10, ncol=3)

# Save plot
plt.tight_layout()
plt.savefig('volatility_cone_dynamic_test.png', dpi=300)
plt.show()
