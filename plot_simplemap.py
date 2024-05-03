import dash
from dash import dcc, html
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='example-map', figure={
        'data': [{
            'type': 'scattermapbox',
            'lat': ['40.7128'],
            'lon': ['-74.0060'],
            'mode': 'markers',
            'marker': {'size': 14}
        }],
        'layout': {
            'mapbox': {
                'accesstoken': "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A",
                'center': {'lat': 40.7128, 'lon': -74.0060},
                'zoom': 10
            },
            'margin': {"r": 0, "t": 0, "l": 0, "b": 0}
        }
    })
])

if __name__ == '__main__':
    app.run_server(debug=True)
