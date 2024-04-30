import dash
from dash import html
import dash_leaflet as dl

app = dash.Dash(__name__)

app.layout = html.Div([
    dl.Map([
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
])

if __name__ == '__main__':
    app.run_server(debug=True, port=1234)
