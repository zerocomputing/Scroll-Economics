import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

pd.set_option('display.max_columns', None)  # Display all columns

# Read the CSV file into a DataFrame
file_path = 'Datasets/Scroll Transactions_RawData_Scrollscan_29012024.csv'
df = pd.read_csv(file_path)

# Extract the selected columns into a new DataFrame and drop empy rows
cols = ['L1DataFee', 'ExecutionFee', 'Block']
df = df[cols].dropna()

# Extract ETH and $ values for 'L1DataFee'
df['L1DataFee_ETH'] = df[cols[0]].str.extract(r'(\d+\.\d+) ETH').astype(float)
df['L1DataFee_USD'] = df[cols[0]].str.extract(r'\((\$[\d.]+)\)').replace('[\$,]', '', regex=True).astype(float)

# Extract ETH and $ values for 'ExecutionFee'
df['ExecutionFee_ETH'] = df[cols[1]].str.extract(r'(\d+\.\d+) ETH').astype(float)
df['ExecutionFee_USD'] = df[cols[1]].str.extract(r'\((\$[\d.]+)\)').replace('[\$,]', '', regex=True).astype(float)

# Drop the old columns
df.drop(['L1DataFee', 'ExecutionFee'], axis=1, inplace=True)

# Group by block and sum the fees
df = df.groupby('Block')[['L1DataFee_USD', 'ExecutionFee_USD']].sum().reset_index()

# Calculate the mean for each fee column
average_fee_per_block = df[['L1DataFee_USD', 'ExecutionFee_USD']].mean()

print("Average L1DataFee per block (USD):", average_fee_per_block['L1DataFee_USD'])
print("Average ExecutionFee per block (USD):", average_fee_per_block['ExecutionFee_USD'])

'''
PLOTLY VISUALIZATION
'''
# Create Dash app
app = Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    dcc.Graph(id='line-chart'),
    html.Div(id='dummy-trigger', style={'display': 'none'})  # Hidden dummy trigger
])

# Callback to update the chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('dummy-trigger', 'children')]  # Use the hidden dummy trigger as Input
)
def update_chart(trigger):
    # Create a line chart
    fig = go.Figure()

    for column in ['L1DataFee_USD', 'ExecutionFee_USD']:
        fig.add_trace(go.Scatter(x=df['Block'], y=df[column], mode='lines', name=column, line_shape='spline'))

    fig.update_layout(
        title='L1 Data Fee and Execution Fee in USD',
        xaxis_title='Block',
        yaxis_title='Fee (USD)',
        height=1000,
        width=2000,
        xaxis=dict(
            tickformat=',d'  # Display tick labels as whole numbers with a comma as a separator
        )
    )

    # Customize hover text to display 'Block' and 'Fee'
    fig.update_traces(
        hovertemplate='Block: %{x}<br>Fee: %{y:.2f} USD',
        selector=dict(type='scatter')
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
