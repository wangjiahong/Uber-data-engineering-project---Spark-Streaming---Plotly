import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import os

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    path = './sparkoutput'  # Update to your actual output directory
    try:
        all_files = os.listdir(path)
        latest = max([os.path.join(path, basename) for basename in all_files], key=os.path.getmtime)
        df = pd.read_csv(latest)
    except Exception as e:
        print(f"Error reading data: {e}")
        return go.Figure()  # Returns an empty plot if there's an error

    # Initialize a figure with Plotly go.Figure
    fig = go.Figure()

    # Add Total Rides bar
    fig.add_trace(
        go.Bar(
            x=df['location'],
            y=df['total_rides'],
            name='🚗 Total Rides',  # Emoji added to label
            marker=dict(color='rgb(55, 83, 109)'),  # Specify bar color
            yaxis='y'
        )
    )

    # Add Average Fare bar
    fig.add_trace(
        go.Bar(
            x=df['location'],
            y=df['avg_fare'],
            name='💵 Average Fare',  # Emoji added to label
            marker=dict(color='rgb(26, 118, 255)'),  # Specify bar color
            yaxis='y2'
        )
    )

    # Update the layout to handle dual y-axes and group bars
    fig.update_layout(
        title='Ride Data Aggregations by Location',
        xaxis=dict(title='Location'),
        yaxis=dict(
            title='Total Rides',
            side='left'  # Position this y-axis to left
        ),
        yaxis2=dict(
            title='Average Fare',
            overlaying='y',
            side='right',  # Position this y-axis to right
            rangemode='tozero'
        ),
        legend=dict(x=0.01, y=0.99, orientation='h'),  # Adjust legend to be horizontal at the top
        barmode='group'  # Ensure bars are grouped side by side
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
