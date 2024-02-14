from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets we are interested in trading
        self.tickers = ["AAPL", "SQQQ"]

    @property
    def assets(self):
        # Return the list of asset tickers
        return self.tickers

    @property
    def interval(self):
        # Define the data interval for analysis, using 1day for daily strategy
        return "1day"

    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {"AAPL": 0, "SQQQ": 0}

        # Gather MACD and RSI data for AAPL
        macd_data = MACD("AAPL", data["ohlcv"], fast=12, slow=26)
        rsi_data = RSI("AAPL", data["ohlcv"], length=14)

        if macd_data is not None and rsi_data is not None:
            macd_histogram = macd_data["histogram"]
            latest_rsi = rsi_data[-1]

            # Determine the MACD trend, checking if the histogram is positive
            macd_trend_up = macd_histogram[-1] > 0

            # Check if RSI indicates AAPL is not overbought
            is_not_overbought = latest_rsi < 70

            # If indicators suggest an upward trend and not overbought, allocate to AAPL
            if macd_trend_up and is_not_overbought:
                allocation_dict["AAPL"] = 0.7  # Allocate 70% to AAPL
                
            # In case the market is likely going down, allocate some to SQQQ as a hedge
            if not macd_trend_up or latest_rsi > 70:  # If downward trend or overbought
                allocation_dict["SQQQ"] = 0.3  # Allocate 30% to SQQQ for hedging

        return TargetAllocation(allocation_dict)