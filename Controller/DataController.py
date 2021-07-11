import configparser
import pandas as pd

class DataController:
    def DataChunks(self,cols,file):
        return pd.read_csv('Resources/'+file,chunksize=1000,parse_dates=True,usecols=cols)

    def prepareData(self,df):
        # load needed columns
        df = df[["date", "open", "high", "low", "close"]]
        #reverse data oldest to newest date
        df = df.iloc[::-1]
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return  df

    def getDataFile(self):
        config = configparser.ConfigParser()
        config.read('config.properties')
        return config.get("DataFile", "file")
