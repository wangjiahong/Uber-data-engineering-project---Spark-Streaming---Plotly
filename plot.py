import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import pandas as pd
import plotly.graph_objs as go
import os

app = dash.Dash(__name__)

def get_latest_csv(directory):
    """Get the latest CSV file from a specified directory."""
    all_files = os.listdir(directory)
    latest_file = max([os.path.join(directory, basename) for basename in all_files])
    return pd.read_csv(latest_file)

map_component = dl.Map(id='map', style={'width': '1500px', 'height': '500px'}, center=[40.7128, -74.0060], zoom=11, children=[dl.TileLayer()])

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
    dcc.Interval(id='fade-interval', interval=1000, n_intervals=1),  # Interval for fading effect
    html.Div([map_component], style={'marginTop': 20})
])

@app.callback(
    [Output('live-update-graph', 'figure'), Output('map', 'children')],
    [Input('interval-component', 'n_intervals'), Input('fade-interval', 'n_intervals')])
def update_graph_live(n, fade_n):
    df = get_latest_csv('./sparkoutput')
    df['location'] = df['location'].replace({'Suburbs': '🏡 Suburbs', 'Downtown': '🏙️ Downtown', 'Airport': '✈️ Airport'})
    locations_df = get_latest_csv('./mapoutput')

    max_fade_intervals = 10  # Total intervals for fading
    opacity = max(0, 1 - fade_n / max_fade_intervals)  # Calculate current opacity
    if fade_n >= max_fade_intervals:
        opacity = 0  # Ensure the markers are invisible after the fade out

    markers = [
        dl.Marker(
            position=[row['starting_location_lat'], row['starting_location_lon']],
            opacity=opacity,  # Apply calculated opacity
            children=[
                dl.Tooltip(row['starting_location_name']),
                dl.Popup(f"This is {row['starting_location_name']}")
            ]
        ) for index, row in locations_df.iterrows()
    ]

    map_children = [dl.TileLayer()] + markers

    data = [
        go.Bar(x=df['location'], y=df['total_rides'], name='🚗 Total Rides', yaxis='y1'),
        go.Bar(x=df['location'], y=df['avg_fare'], name='💵 Average Fare', yaxis='y2')
    ]

    layout = go.Layout(
        title='Ride Data Aggregations by Location',
        xaxis=dict(title='Location'),
        yaxis=dict(title='Total Rides', side='left'),
        yaxis2=dict(title='Average Fare', overlaying='y', side='right'),
        barmode='relative'
    )

    return {'data': data, 'layout': layout}, map_children

if __name__ == '__main__':
    app.run_server(debug=True)
