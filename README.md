# Volatility Cone Data Analysis 

## Overview
This project analyzes the volatility characteristics of financial markets by comparing **historical implied volatility** (VIX) and **realized volatility** (SPY historical data). Using VIX data to construct rolling volatility cones and SPY options data to compute implied volatility, the project examines whether VIX and SPY implied volatility are consistent. This analysis reveals potential discrepancies between overall market volatility expectations and specific asset volatility expectations, helping to explore market sentiment, identify potential risks, and provide insights into market expectations.

## Objectives
1. **Historical Implied Volatility (VIX) Analysis**:
   - Calculate **rolling volatilities** over different time windows (21, 42, 63, 126, 189 days) using VIX data.
   - Compute quantiles (25%, 50%, 75%) to construct a volatility cone and analyze the historical range of implied volatility expectations.

2. **Realized Volatility (SPY Historical Data) Analysis:**:
   - Retrieve SPY historical data and calculate realized volatility using daily returns..
   - Compare SPY realized volatility levels with historical implied volatility quantiles from VIX.

3. **Visualization**:
    - Overlay historical implied volatility (VIX) and SPY realized volatility on a single graph.
   - Dynamically adjust chart parameters (e.g., legend positioning, axis ranges) for improved visualization.

4. **Trading Strategy Insights**:
   - Use the volatility cone to develop and simulate potential trading strategies, such as short-term option selling or long-term volatility arbitrage.



## Directory Structure
```plaintext
volatility-cone/
├── data/                       # Folder for data files
│   └── vix_data.csv            # VIX historical implied volatility data
├── src/                        # Source code folder
│   └── volatility_cone.py      # Module for volatility cone calculations and analysis
├── results/                    # Folder for output results and charts
│   ├── volatility_cone.csv     # Processed results of volatility cone data
│   └── volatility_cone.png     # Generated graph
└── README.md                   # Project description file
```


## Data Collection

This project collects and processes two main datasets: **VIX data** and **SPY historical data**.
- The data of them can be retrieved using the `yfinance` library from Yahoo Finance.

**VIX Data**
```python
import yfinance as yf
print("download VIX data...")
vix_data = yf.download('^VIX', start='YYYY-MM-DD', end='YYYY-MM-DD')
```
**SPY Data**
```python
print("Downloading SPY data...")
spy_data = yf.download('SPY', start='YYYY-MM-DD', end='YYYY-MM-DD')
```
ALSO CAN check VIX data from the CBOE website . The VIX data will represent overall market implied volatility.

 [Google](https://www.cboe.com)


## Analysis Workflow

1. **Data Cleaning and Processing**
   - Download VIX data (^VIX) to represent historical implied volatility and SPY data for realized volatility.
   - Clean the data by removing missing values using .dropna().

2. **Calculate Historical Volatility Cone**
   - Use rolling windows (21, 42, 63, 126, 189 days) to calculate annualized historical volatilities for VIX.
   - Compute key quantiles (25%, 50%, 75%) for each time frame to construct the historical implied volatility cone.

3. **Calculate Realized Volatility**:
   - Calculate SPY's realized volatility using daily returns and annualize it for each rolling window.

4. **Overlay and Visualize**:
   - Plot VIX rolling volatility quantiles (solid lines) and SPY realized volatility (dashed lines) on the same graph.
   - Dynamically adjust right-axis ranges and chart legends to ensure readability.

5. **Trading Strategy Development**:
   - Use the volatility cone to analyze implied and realized volatility discrepancies.
   - Simulate strategies like short-term option selling (when implied volatility exceeds realized) and long-term straddle buying.


## Example Chart and Key Insights

The output of this project is a volatility cone chart, which compares VIX rolling volatilities and SPY realized volatilities.

**Example Output**:

1. Volatility Trends:
   - The VIX rolling volatility lines (solid) show the dynamic changes in market expectations over different timeframes.
   - Realized volatility (dashed lines) provides a measure of SPY's actual market volatility.
     
2. Quantile Analysis:
   - VIX quantiles (25%, 50%, 75%) show the historical range of market volatility expectations.
   - The chart evaluates whether current VIX levels fall within historical norms.

3. Discrepancy Detection:
   - Periods where SPY's realized volatility is significantly below VIX quantiles may suggest opportunities to sell options.
   - Conversely, when realized volatility exceeds implied volatility, it may indicate undervalued volatility.


---
