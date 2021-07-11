import pandas as pd
from Controller import MovingAvgController as mas
from Controller import DrawPlot as dp

class DataController:
    def DataChunks(self,cols):
        return pd.read_csv('../Resources/Binance_BTCUSDT_minute.csv',chunksize=1000,parse_dates=True,usecols=cols)

    def prepareData(self,df):
        # load needed columns
        df = df[["date", "open", "high", "low", "close"]]
        #reverse data oldest to newest date
        df = df.iloc[::-1]
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return  df
