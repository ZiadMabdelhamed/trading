import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

from Controller import MovingAvgController as MAController
from Controller import DataController as dataController
from Model import Figure as fig
from Controller import DrawPlot as dp
import datetime


DC = dataController.DataController()
MA = MAController.MovingAvgController()
Fig = fig.Figure()

cols =['date', 'open', 'high', 'low', 'close']
data = DC.DataChunks(cols)
#get first chunk
df = next(data)
df = DC.prepareData(df)

newestDate = datetime.datetime.utcfromtimestamp(df['date'].head(1).values[0].astype('O') / 1e9)


def start(df):
    df['MA14'] = MA.CalculateMA14(df)
    df['MA50'] = MA.CalculateMA50(df)
    df['MA100'] = MA.CalculateMA100(df)
    df['MA200'] = MA.CalculateMA200(df)
    df["Marker"] = MA.CalculateSignalMarker(df)
    df["Symbol"]  = MA.CalculateSignalSymbol(df)
    df["Color"]  = MA.CalculateSignalColor(df)
    df["SignalType"]  = MA.CalculateSignalType(df)
    return df

df = start(df)
Fig.getData().append(dp.DrawCandleStick(df))
Fig.getData().append(dp.DrawMA(df['date'],df['MA14'],'blue','MA 14'))
Fig.getData().append(dp.DrawMA(df['date'],df['MA50'],'orange','MA 50'))
Fig.getData().append(dp.DrawMA(df['date'],df['MA100'],'black','MA 100'))
Fig.getData().append(dp.DrawMA(df['date'],df['MA200'],'grey','MA 200'))
Fig.getData().append(dp.DrawMarker(df[['date','Marker','Symbol','Color','SignalType']],'marker'))

Fig.setLayout(dp.layout())



app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True,figure={"data": Fig.data,"layout":Fig.layout},
                  config={
                      'staticPlot': False,  # True, False
                      'scrollZoom': True,  # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,  # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': False,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                  }
                  ),
        dcc.Interval(
            id='interval-component',
            interval=1 * 100000,  # in milliseconds
            n_intervals=0,
            disabled = True,
            max_intervals=2
        )
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('live-graph', 'relayoutData')])
def update_graph_scatter(relayout_data):
    loadNewFig=False
    if relayout_data is not  None:
        if 'xaxis.range[0]' in relayout_data :
            print('graph limit : '+relayout_data['xaxis.range[0]'])
            startTimeOfChart = datetime.datetime.strptime(relayout_data['xaxis.range[0]'], '%Y-%m-%d %H:%M:%S.%f')
            global newestDate
            global df
            global data
            global Fig

            if startTimeOfChart < newestDate:
                nextDataChunk = next(data)
                nextDataChunk = DC.prepareData(nextDataChunk)
                newestDate = datetime.datetime.utcfromtimestamp(nextDataChunk['date'].head(1).values[0].astype('O') / 1e9)
                prevDataChunk = df

                Fig.data[0] = dp.DrawCandleStick(df.append(nextDataChunk))


                df14 = nextDataChunk.append(prevDataChunk.head(14))
                df14['MA14'] = MA.CalculateMA14(df14)
                Fig.data[1] = dp.DrawMA(df['date'].append(df14['date']),df['MA14'].append(df14['MA14']),'blue','MA 14')

                df50 = nextDataChunk.append(prevDataChunk.head(50))
                df50['MA50'] = MA.CalculateMA50(df50)
                Fig.data[2] = dp.DrawMA(df['date'].append(df50['date']),df['MA50'].append(df50['MA50']),'orange','MA 50')


                df100 = nextDataChunk.append(prevDataChunk.head(100))
                df100['MA100'] = MA.CalculateMA100(df100)
                Fig.data[3] = dp.DrawMA(df['date'].append(df100['date']),df['MA100'].append(df100['MA100']),'black','MA 100')


                df200 = nextDataChunk.append(prevDataChunk.head(200))
                df200['MA200'] = MA.CalculateMA200(df200)
                Fig.data[4] = dp.DrawMA(df['date'].append(df200['date']),df['MA200'].append(df200['MA200']),'grey','MA 200')

                nextDataChunk['MA14'] = df14['MA14']
                nextDataChunk['MA50'] = df50['MA50']
                Fig.data[5] = dp.DrawMarker(df[['date', 'Marker', 'Symbol', 'Color', 'SignalType']].
                                            append(MA.CalculateSignal(nextDataChunk))
                                            , 'marker')

                ########
                allData = df200.append(df100).append(df50).append(df14).append(df)
                df = allData
                loadNewFig = True
    if loadNewFig:
        return {"data": Fig.data,"layout":Fig.layout}
    else:
        return  dash.no_update


if __name__ == '__main__':
    app.run_server(host='127.1.1.1', port=8091 ,debug=False)