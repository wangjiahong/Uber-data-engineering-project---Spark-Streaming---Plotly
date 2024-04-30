import dash
from dash import dcc, html
import dash_leaflet as dl
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os
from plotly.subplots import make_subplots

app = dash.Dash(__name__)

# Define the map component
def create_map():
    return dl.Map([
        dl.TileLayer(),  # This uses the default OpenStreetMap tiles
        dl.Marker(position=[40.7128, -74.0060], children=[
            dl.Tooltip("New York City"),
            dl.Popup("This is NYC")
        ]),
        dl.Marker(position=[40.7505, -73.9934], children=[
            dl.Tooltip("Madison Square Garden"),
            dl.Popup("Home of the New York Knicks and New York Rangers")
        ]),
        dl.Marker(position=[40.8296, -73.9262], children=[
            dl.Tooltip("Yankee Stadium"),
            dl.Popup("This is where the New York Yankees play")
        ])
    ], style={'width': '1000px', 'height': '500px'}, center=[40.7128, -74.0060], zoom=10)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=300,  # in milliseconds
        n_intervals=0
    ),
    # Add the map component here
    html.Div([
        create_map()
    ], style={'marginTop': 20})  # Add some top margin for better spacing
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
            yaxis='y1'
        ),
        go.Bar(
            x=df['location'],
            y=df['avg_fare'],
            name='💵 Average Fare',  # Emoji added to label
            yaxis='y2'
        )
    ]

    layout = go.Layout(
        title='Ride Data Aggregations by Location',
        xaxis=dict(title='Location'),
        yaxis=dict(
            title='Total Rides',
            side='left',
        ),
        yaxis2=dict(
            title='Average Fare',
            overlaying='y',
            side='right',
        ),
        barmode='relative'
    )

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
