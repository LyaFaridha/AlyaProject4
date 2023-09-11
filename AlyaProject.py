from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

app.title = "MCM7003 Data Visualization Interactive Demo"

# Load data from the provided URL
data_url = "https://raw.githubusercontent.com/LyaFaridha/AlyaProject4/main/df_arabica_clean.csv"
df = pd.read_csv(data_url)

# Create a bar chart for the 'Country of Origin' counts
country_counts = df['Country of Origin'].value_counts()
fig_country_counts = px.bar(country_counts, x=country_counts.index, y=country_counts.values)

fig_country_counts.update_layout(
    xaxis_title='Country of Origin',
    yaxis_title='Count',
    title={'text': 'Distribution of Country of Origins', 'x': 0.5}
)

# Create the first scatter plot
fig1 = px.scatter(df, x='Aroma', y='Flavor', color='Country of Origin',
                 labels={'Aroma': 'Aroma', 'Flavor': 'Flavor', 'Country of Origin': 'Country of Origin'},
                 title='Relationship between Aroma and Flavor Attributes by Country of Origin')
fig1.update_traces(
    marker=dict(size=10),
    selector=dict(mode='markers')
)

# Create the second box plot
fig2 = px.box(df, x='Processing Method', y=['Aroma', 'Flavor'],
             labels={'variable': 'Attribute', 'value': 'Rating', 'Processing Method': 'Processing Method'},
             title='Comparison of Aroma and Flavor Attributes across Processing Methods')

app.layout = html.Div(
    [
        html.H1("Data Visualization"),
        dcc.Checklist(
            id='show-chart',
            options=[
                {'label': 'Show Country Counts Chart', 'value': 'show-country-counts'}
            ],
            value=[],  # Initialize with no selected options
        ),
        dcc.RadioItems(
            id='select-graph',
            options=[
                {'label': 'Country Counts', 'value': 'country-counts'},
                {'label': 'Relationship between Aroma and Flavor', 'value': 'aroma-flavor'},
                {'label': 'Comparison of Aroma and Flavor Attributes', 'value': 'aroma-flavor-comparison'}
            ],
            value='country-counts',
            labelStyle={'display': 'block'}
        ),
        dcc.Graph(id='graph-output'),
    ]
)

@app.callback(
    Output(component_id='graph-output', component_property='figure'),
    Input(component_id='show-chart', component_property='value'),
    Input(component_id='select-graph', component_property='value')
)
def update_chart(show_chart, select_graph):
    graphs = []  # List to hold the selected graphs

    if 'show-country-counts' in show_chart:
        if select_graph == 'country-counts':
            return fig_country_counts

    if select_graph == 'aroma-flavor':
        return fig1
    elif select_graph == 'aroma-flavor-comparison':
        return fig2

    return {}

if __name__ == '__main__':
    app.run_server(debug=True)
