import  numpy as np

class MovingAvgController:

    def CalculateMA14(self, df):
        return df['close'].rolling(14).mean()

    def CalculateMA50(self, df):
        return df['close'].rolling(50).mean()

    def CalculateMA100(self, df):
        return df['close'].rolling(100).mean()

    def CalculateMA200(self, df):
        return df['close'].rolling(200).mean()

    def CalculateSignalMarker(self,df):
        d = 3
        return np.where(df["MA14"] > df["MA50"], df["high"] + d, df["low"] - d)

    def CalculateSignalSymbol(self,df):
        return np.where(df["MA14"] > df["MA50"], "triangle-up", "triangle-down")

    def CalculateSignalColor(self,df):
        return np.where(df["MA14"] > df["MA50"], "green", "red")

    def CalculateSignalType(self,df):
        return np.where(df["MA14"] > df["MA50"], "Buy", "Sell")

    def CalculateSignal(self,df):
        d = 3
        df["Marker"] = np.where(df["MA14"] > df["MA50"], df["high"] + d, df["low"] - d)
        df["Symbol"] = np.where(df["MA14"] > df["MA50"], "triangle-up", "triangle-down")
        df["Color"] = np.where(df["MA14"] > df["MA50"], "green", "red")
        df["SignalType"] = np.where(df["MA14"] > df["MA50"], "Buy", "Sell")
        return df[['date', 'Marker', 'Symbol', 'Color', 'SignalType']]








