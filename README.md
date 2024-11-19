# Volatility Cone Data Analysis 

## Overview
This project analyzes the volatility characteristics of financial markets by comparing **historical implied volatility** (VIX) and **implied volatility** (SPY options). Using VIX data to construct rolling volatility cones and SPY options to compute implied volatility, it examines whether VIX and SPY implied volatility are consistent, revealing potential discrepancies between overall market volatility expectations and specific asset volatility expectations. Additionally, the analysis aims to explore market sentiment, identify potential risks, and provide insights into market expectations. 

## Objectives
1. **Historical Volatility (VIX) Analysis**:
   - Calculate **rolling volatilities** over different time windows (21, 63, 126 days) using VIX data.
   - Compute quantiles (10%, 50%, 90%) to construct a volatility cone and analyze the historical range of implied volatility expectations.

2. **Implied Volatility (SPY Options) Analysis**:
   - Retrieve SPY options data and calculate implied volatility using the **Black-Scholes model**.
   - Compare SPY implied volatility quantiles with historical implied volatility quantiles from VIX.

3. **Visualization**:
    - Overlay historical implied volatility (VIX) and SPY implied volatility quantiles on a single graph.
   - Provide insights into market sentiment and identify deviations from historical norms.



## Directory Structure
```plaintext
volatility-cone/
├── data/                       # Folder for data files
│   └── vix_data.csv            # VIX historical implied volatility data
├── src/                        # Source code folder
│   └── main.py                 # Module for volatility cone calculations and analysis
├── results/                    # Folder for output results and charts
│   ├── VIX_volatility.csv 
│   └── volatility_cone.png #Generated graphs and analysis outputs.
├── README.md                   # Project description file
└── requirements.txt            # Project dependency file
```


## Data Collection

This project collects and processes two main datasets: **VIX data** and **SPY options data**.

**VIX Data**
- VIX data is retrieved using the `yfinance` library from Yahoo Finance.
```python
import yfinance as yf

print("download VIX data...")
vix_data = yf.download('^VIX', start='YYYY-MM-DD', end='YYYY-MM-DD')
```
**SPY Data**
-
 
#### **ALSO CAN check VIX data from the CBOE website and save it as vix_data.csv. The VIX data will represent overall market implied volatility.**

 [Google](https://www.cboe.com)


## Analysis Workflow

1. **Data Cleaning and Processing**
   - Download VIX data (`^VIX`) to represent historical volatility.
   - Remove missing values using `.dropna()` to ensure data consistency.

2. **Calculate Historical Volatility Cone**
   - Use 1-month (21 days), 3-month (63 days), and 6-month (126 days) rolling windows to calculate annualized historical volatilities.
   - Compute quantiles (10%, 50%, 90%) for each time frame to construct the historical volatility cone.

3. **Construct Implied Volatility Cone**
   - Retrieve SPY options data and calculate implied volatilities using the Black-Scholes model.
   - Compute quantiles (10%, 50%, 90%) for implied volatility to construct the implied volatility cone.

4. **Visualization**
   - Save the results to an output folder for further analysis.

## Example Result

Below is the output of the project:

![Volatility Cone Result](result/volatility_cone.png)


---
