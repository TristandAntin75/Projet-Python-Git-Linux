import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime, time, timedelta
import plotly.graph_objs as go

# Load data
data = pd.read_csv('CAC_values.txt', header=None, delimiter=',')
data.columns = ['datetime', 'value']
data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')
data = data.set_index('datetime')

# Set up app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('CAC40 Dashboard'),
    html.Div([
        html.H3('Last CAC40 Value'),
        html.P(id='last-cac-value')
    ]),
    dcc.Graph(id='cac-graph'),
    html.Div([
        html.H3('Daily Report'),
        html.Table(id='daily-report')
    ]),
    dcc.Interval(
        id='interval-component',
        interval=300000,  # Update every 5 minutes
        n_intervals=0
    )
])


@app.callback(Output('last-cac-value', 'children'), [Input('interval-component', 'n_intervals')])
def update_last_cac_value(n):
    last_cac_value = round(data['value'][-1], 2)
    return f'{last_cac_value} €'


@app.callback(Output('cac-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph(n):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['value'], mode='lines', name='CAC40'))
    fig.update_layout(title='CAC40 Time Series', xaxis_title='Date', yaxis_title='Value')
    return fig


@app.callback(Output('daily-report', 'children'), [Input('interval-component', 'n_intervals')])
def update_daily_report(n):
    today = datetime.now().date()
    report_date = datetime.combine(today, time(20, 0))
    if datetime.now() >= report_date:
        report_data = data[today.strftime('%Y-%m-%d')]
        open_price = report_data['value'][0]
        close_price = report_data['value'][-1]
        daily_return = round((close_price / open_price - 1) * 100, 2)
        daily_volatility = round(report_data['value'].pct_change().std() * 100, 2)
        return html.Tr([
            html.Td('Open Price'), html.Td(f'{open_price} €'),
            html.Td('Close Price'), html.Td(f'{close_price} €'),
            html.Td('Daily Return'), html.Td(f'{daily_return}%'),
            html.Td('Daily Volatility'), html.Td(f'{daily_volatility}%')
        ])
    else:
        return html.Tr([
            html.Td('No report available')
        ])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)

