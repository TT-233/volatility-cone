# Volatility Cone Data Analysis Project

We aims to analyze volatility characteristics in financial markets using the Volatility Cone model. By collecting historical price data and implied volatility data for options, we construct volatility cones over different time periods to aid in risk management and trading strategy decisions.

## Project Background
A volatility cone is a tool used to predict the range of future price fluctuations based on historical data and market expectations of future volatility. By analyzing volatilities over different time frames, it provides a more reliable risk forecast. In this project, we use the historical price data of the S&P 500 index and the VIX index as a proxy for implied market volatility to construct the volatility cone model.

## Features
- **Historical Price Data Collection**: Retrieve historical data of the S&P 500 index from Yahoo Finance to calculate historical volatilities over different time periods.
- **Implied Volatility Data Collection**: Use VIX data from CBOE as a base for constructing the implied volatility cone.
- **Volatility Cone Calculation**: Construct 1-month, 3-month, and 6-month historical volatility cones and implied volatility cones.
- **Visualization and Analysis**: Display trends in historical and implied volatilities through charts for intuitive analysis.
   
## Directory Structure
```plaintext
volatility-cone/
├── data/                       # Folder for data files
│   ├── sp500_data.csv          # Historical price data of the S&P 500
│   └── vix_data.csv            # VIX historical implied volatility data
├── src/                        # Source code folder
│   └── main.py                 # Module for volatility cone calculations and analysis
├── results/                    # Folder for output results and charts
│   ├── VIX_volatility.csv 
│   └── vix_volatility_cone.png #Generated graphs and analysis outputs.
├── README.md                   # Project description file
└── requirements.txt            # Project dependency file
```


## Data Collection

1. Collect Historical Price Data

**Use the yfinance library to download historical price data of the S&P 500 index from Yahoo Finance.**
   ```bash
  import yfinance as yf

  # Retrieve historical data for the S&P 500 index
  sp500 = yf.Ticker("^GSPC")
  data = sp500.history(period="5y")  # Get the past 5 years of data
  data.to_csv("data/sp500_data.csv")  # Save as CSV file
 ```

2. Collect Implied Volatility Data
 
 **Download VIX data from the CBOE website and save it as vix_data.csv. The VIX data will represent overall market implied volatility.**

 [Google](https://www.cboe.com)


## Analysis Workflow

1. **Data Cleaning and Processing**

 - Format the retrieved S&P 500 and VIX data, ensuring consistency in the time series.
 - Remove missing values and outliers, and standardize date formats.

2. **Calculate Historical Volatility Cone**

 - Calculate 1-month, 3-month, and 6-month historical volatilities using a rolling window method and annualize the results.
 - Plot the volatility cone for each time frame to analyze the historical volatility range.

3. **Construct Implied Volatility Cone**

 - Use the VIX data to construct the implied volatility cone.
 - Compare the implied volatility cone with the historical volatility cone to analyze differences between market expectations and historical volatilities.

4. **Visualization**

 - Use Matplotlib to plot both historical and implied volatility cones.
 - Save the charts to the results folder.

## Example Result

Below is the output of the project:

![Volatility Cone Result](results/vix_volatility_cone.png)
