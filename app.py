from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server  # Required for Render

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Grapes"],
    "Amount": [4, 2, 5, 3]
})

app.layout = html.Div([
    html.H1("My Dash App"),
    dcc.Graph(id="bar-chart"),
])

@callback(Output("bar-chart", "figure"), Input("bar-chart", "id"))
def update_chart(_):
    return px.bar(df, x="Fruit", y="Amount")

if __name__ == "__main__":
    app.run(debug=True)
