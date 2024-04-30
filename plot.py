import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=300,  # in milliseconds
        n_intervals=0
    )
])

def add_emojis_to_locations(df):
    emoji_map = {
        'Suburbs': '🏡 Suburbs',
        'Downtown': '🏙️ Downtown',
        'Airport': '✈️ Airport'
    }
    df['location'] = df['location'].map(emoji_map)
    return df

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    path = './sparkoutput'
    all_files = os.listdir(path)
    latest = max([os.path.join(path, basename) for basename in all_files])
    df = pd.read_csv(latest)
    df = add_emojis_to_locations(df)


    data = [
        go.Bar(
            x=df['location'],
            y=df['total_rides'],
            name='🚗 Total Rides',  # Emoji added to label
            # marker=dict(color='rgb(55, 83, 109)'),  # Specify bar color
            yaxis='y1'
        ),
        go.Bar(
            x=df['location'],
            y=df['avg_fare'],
            name='💵 Average Fare',  # Emoji added to label
            # marker=dict(color='rgb(26, 118, 255)'),  # Specify bar color
            yaxis='y2'
        )
    ]

    layout = go.Layout(
        title='Ride Data Aggregations by Location',
        xaxis=dict(title='Location'),
        yaxis=dict(
            title='Total Rides',
            side='left',  # Position this y-axis to left
            # rangemode='tozero'
        ),
        yaxis2=dict(
            title='Average Fare',
            overlaying='y',
            side='right',  # Position this y-axis to right
            # rangemode='tozero'
        ),
        # legend=dict(x=0.01, y=0.99, orientation='h'),  # Adjust legend to be horizontal at the top
        barmode='relative'  # Group bars to show side by side
    )

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
