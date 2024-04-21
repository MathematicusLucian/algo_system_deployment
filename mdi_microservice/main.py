import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
from src.services.strategy.macd import MACD
import matplotlib.pyplot as plt
import plotly.graph_objects as go

base="USD"
second_currency="BTC"
period="1yr"
fast=12
slow=26
signal=9
ta_sample_data = "./src/services/strategy/datas.csv"
btc_historic_data = "./src/services/strategy/Binance_BTCGBP_d.csv"

def append_rsi_to_df(df: pd.DataFrame):
    # df["RSI"]=ta.rsi(close=df.Close,length=10)
    df.ta.rsi(length=100, append=True)
    # plt.plot(df.Date, df.RSI)

def append_sma_to_df(df: pd.DataFrame):
    # df["SMA"]=ta.rsi(close=df.Close,length=10)
    df.ta.sma(length=100, append=True)
    # plt.plot(df.Date, df.SMA)

def plot(df: pd.DataFrame, indicator: str):
    if indicator == "rsi":
        plt.plot(df.Date, df.RSI_100)
    elif indicator == "sma":
        plt.plot(df.Date, df.SMA_100)

def create_plot_graph(df: pd.DataFrame):
    plt.plot(df.Date, df.Close)
    append_rsi_to_df(df)
    append_sma_to_df(df)
    df.ta.indictators()
    plot(df, "rsi")
    plot(df, "sma")
    plt.show()

macd_obj = MACD(base, second_currency, period, fast, slow, signal)
df = macd_obj.df
# print(df)
fig = go.Figure(data=[go.Candlestick(
    x=df.Date,
    open=df.Open,
    high=df.High,
    low=df.Low,
    close=df.Close
)])
fig.show()

# print("\n\n"+macd_obj.macd.to_json(orient='table'))
# print("\n\n"+macd_obj.macd.to_json(orient ='records'))
# print(f"\n\n")
# print(macd_obj.df)
# print(f"\n\n")
# print(macd_obj.macd)

# print(f"\n\n{macd_obj.macdh_config}")
# print(f"\n\n{macd_obj.macds_config}")

# macd_obj.create_fig()

# window = 12
# df[f"roc_{window}"] = momentum.ROCIndicator(close=df["Close"], window=window).roc()

# # Create your own Custom Strategy
# CustomStrategy = ta.Strategy(
#     name="Momo and Volatility",
#     description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
#     ta=[
#         {"kind": "sma", "length": 50},
#         {"kind": "sma", "length": 200},
#         {"kind": "bbands", "length": 20},
#         {"kind": "rsi"},
#         {"kind": "macd", "fast": 8, "slow": 21},
#         {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
#     ]
# )
# # To run your "Custom Strategy"
# df.ta.strategy(CustomStrategy)