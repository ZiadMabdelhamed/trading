import plotly.graph_objs as go

def DrawCandleStick(df):
   return  {
        'x': df['date'],
        'date': df['date'],
        'open': df['open'],
        'close': df['close'],
        'high': df['high'],
        'low': df['low'],
        'type': 'candlestick',
        'name': 'Data',
        'showlegend': False
    }

def DrawMA(date,MA,color,name):
   return  {
        'x': date,
        'y': MA,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1.5,
            'color': color
        },
        'name': name
    }

def DrawMarker(df,name):
   return  {
        'x': df['date'],
        'y': df['Marker'],
        'mode': 'markers',
        'name': 'Signal',
        'marker':
            {
                'size': 5,
                'symbol': df["Symbol"],
                'color': df["Color"]
            },
       'showlegend': False,
       'text':df["SignalType"]
    }


def layout():
    return go.Layout(
        xaxis_rangeslider_visible=False,
        height=650,
        title='crypto pair based on 1 minute period'
    )