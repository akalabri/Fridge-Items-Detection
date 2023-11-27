import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import csv
import time

# Initialize Dash app
app = dash.Dash(__name__)

# Define the global variables
df = pd.read_csv('Fridge_Inventory.csv')
st_milk_inventory = df['St Milk'].iloc[-1]
ch_milk_inventory = df['Ch Milk'].iloc[-1]
sando_inventory = df['Sando'].iloc[-1]
biscuit_inventory = df['Biscuit'].iloc[-1]
chocolate_inventory = df['Chocolate'].iloc[-1]

# Function to update the inventory and add a new row to the CSV file
def update_inventory(selected_item, person_name, quantity):
    global st_milk_inventory, ch_milk_inventory, sando_inventory, biscuit_inventory, chocolate_inventory

    if selected_item == 'st_milk':
        st_milk_inventory += int(quantity)
    elif selected_item == 'ch_milk':
        ch_milk_inventory += int(quantity)
    elif selected_item == 'sando':
        sando_inventory += int(quantity)
    elif selected_item == 'biscuit':
        biscuit_inventory += int(quantity)
    elif selected_item == 'chocolate':
        chocolate_inventory += int(quantity)

    current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")
    new_row = {
        'Date/Time': current_datetime,
        'Person': person_name,
        'St Milk': st_milk_inventory,
        'Ch Milk': ch_milk_inventory,
        'Sando': sando_inventory,
        'Biscuit': biscuit_inventory,
        'Chocolate': chocolate_inventory,
        'Type': 'Add',
    }

    # Append the new row to the CSV file
    with open('Fridge_Inventory.csv', 'a', newline='') as csvfile:
        fieldnames = ['Date/Time', 'Person', 'St Milk', 'Ch Milk', 'Sando', 'Biscuit', 'Chocolate', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(new_row)

    # Read the updated CSV file
    global df
    df = pd.read_csv('Fridge_Inventory.csv')
    return st_milk_inventory, ch_milk_inventory, sando_inventory, biscuit_inventory, chocolate_inventory, df

# Function to generate inventory plot
def generate_inventory_plot(df):
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date/Time'], y=df['St Milk'], mode='lines', name='Strawberry Milk'))
    fig.add_trace(go.Scatter(x=df['Date/Time'], y=df['Ch Milk'], mode='lines', name='Chocolate Milk'))
    fig.add_trace(go.Scatter(x=df['Date/Time'], y=df['Sando'], mode='lines', name='Sando'))
    fig.add_trace(go.Scatter(x=df['Date/Time'], y=df['Biscuit'], mode='lines', name='Biscuit'))
    fig.add_trace(go.Scatter(x=df['Date/Time'], y=df['Chocolate'], mode='lines', name='Chocolate'))
    fig.update_layout(title='Inventory Over Time', xaxis_title='Date', yaxis_title='Quantity')
    return fig

# Define the layout of the app
app.layout = html.Div(id='main-layout', children=[
    html.H1("Fridge Inventory Dashboard", style={'textAlign': 'center'}),

    # Display current inventory
    html.Div([
        html.H2("Current Inventory"),
        html.Table(
            [html.Tr([html.Th("Item"), html.Th("Quantity")], style={'backgroundColor': '#f2f2f2'})] +
            [html.Tr([html.Td("Strawberry Milk"), html.Td(f"{st_milk_inventory}")]),
             html.Tr([html.Td("Chocolate Milk"), html.Td(f"{ch_milk_inventory}")]),
             html.Tr([html.Td("Sando"), html.Td(f"{sando_inventory}")]),
             html.Tr([html.Td("Biscuit"), html.Td(f"{biscuit_inventory}")]),
             html.Tr([html.Td("Chocolate"), html.Td(f"{chocolate_inventory}")])],
            style={'margin': '5px auto', 'textAlign': 'center', 'width': '30%'}
        ),
    ], style={'textAlign': 'center'}),

    # Display the last 5 rows of the CSV file in a table with conditional row background color
    html.Div([
        html.H2("Last 5 Actions"),
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df.columns], style={'backgroundColor': '#f2f2f2'})] +
            # Body with conditional styling
            [
                html.Tr(
                    [
                        html.Td(df.iloc[-5][col])
                        if col != "Type"
                        else html.Td(
                            df.iloc[-5][col],
                            style={"backgroundColor": "green" if df.iloc[-5]["Type"] == "Add" else "orange"},
                        )
                        for col in df.columns
                    ]
                ),
                html.Tr(
                    [
                        html.Td(df.iloc[-4][col])
                        if col != "Type"
                        else html.Td(
                            df.iloc[-4][col],
                            style={"backgroundColor": "green" if df.iloc[-4]["Type"] == "Add" else "orange"},
                        )
                        for col in df.columns
                    ]
                ),
                html.Tr(
                    [
                        html.Td(df.iloc[-3][col])
                        if col != "Type"
                        else html.Td(
                            df.iloc[-3][col],
                            style={"backgroundColor": "green" if df.iloc[-3]["Type"] == "Add" else "orange"},
                        )
                        for col in df.columns
                    ]
                ),
                html.Tr(
                    [
                        html.Td(df.iloc[-2][col])
                        if col != "Type"
                        else html.Td(
                            df.iloc[-2][col],
                            style={"backgroundColor": "green" if df.iloc[-2]["Type"] == "Add" else "orange"},
                        )
                        for col in df.columns
                    ]
                ),
                html.Tr(
                    [
                        html.Td(df.iloc[-1][col])
                        if col != "Type"
                        else html.Td(
                            df.iloc[-1][col],
                            style={"backgroundColor": "green" if df.iloc[-1]["Type"] == "Add" else "orange"},
                        )
                        for col in df.columns
                    ]
                ),
            ],
            style={'margin': '20px auto', 'width': '70%'}
        ),
    ], style={'textAlign': 'center'}),

    # Updating Inventory Section
    html.Div([
        html.H2("Updating Inventory"),
        html.Label("Select Item"),
        dcc.Dropdown(
            id="item-dropdown",
            options=[
                {'label': 'Strawberry Milk', 'value': 'st_milk'},
                {'label': 'Chocolate Milk', 'value': 'ch_milk'},
                {'label': 'Sando', 'value': 'sando'},
                {'label': 'Biscuit', 'value': 'biscuit'},
                {'label': 'Chocolate', 'value': 'chocolate'},
            ],
            value='st_milk'
        ),
        html.Label("Your Name"),
        dcc.Input(id='name-input', type='text', placeholder='Enter your name'),
        html.Label("Quantity"),
        dcc.Input(id='quantity-input', type='number', placeholder='Enter quantity'),
        html.Button('Add', id='update-button', n_clicks=0),
        html.Div(id='update-result'),
    ], style={'textAlign': 'center'}),
    # New section for plotting inventory over time
    html.Div([
        html.H2("Inventory Trends"),
        dcc.Graph(id='inventory-plot', figure=generate_inventory_plot(df))
    ])
], style={'font-family': 'Arial, sans-serif'})


@app.callback(
    [Output('main-layout', 'children'), Output('update-result', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('item-dropdown', 'value'), State('name-input', 'value'), State('quantity-input', 'value')],
    prevent_initial_call=True
)
def update_inventory_callback(n_clicks, selected_item, person_name, quantity):
    if n_clicks > 0:
        updated_st_milk, updated_ch_milk, updated_sando, updated_biscuit, updated_chocolate, updated_df = update_inventory(
            selected_item, person_name, quantity
        )

        # Recreate the entire layout with updated values
        updated_layout = html.Div([
            html.H1("Fridge Inventory Dashboard", style={'textAlign': 'center'}),
            # Display current inventory (updated)
            html.Div([
                html.H2("Current Inventory"),
                html.Table(
                    [html.Tr([html.Th("Item"), html.Th("Quantity")], style={'backgroundColor': '#f2f2f2'})] +
                    [html.Tr([html.Td("Strawberry Milk"), html.Td(f"{updated_st_milk}")]),
                     html.Tr([html.Td("Chocolate Milk"), html.Td(f"{updated_ch_milk}")]),
                     html.Tr([html.Td("Sando"), html.Td(f"{updated_sando}")]),
                     html.Tr([html.Td("Biscuit"), html.Td(f"{updated_biscuit}")]),
                     html.Tr([html.Td("Chocolate"), html.Td(f"{updated_chocolate}")])],
                    style={'margin': '5px auto', 'textAlign': 'center', 'width': '30%'}
                ),
            ], style={'textAlign': 'center'}),

            # Display the last 5 rows of the CSV file in a table with conditional row background color (updated)
            html.Div([
                html.H2("Last 5 Actions"),
                html.Table(
                    # Header
                    [html.Tr([html.Th(col) for col in updated_df.columns], style={'backgroundColor': '#f2f2f2'})] +
                    # Body with conditional styling
                    [
                        html.Tr(
                            [
                                html.Td(updated_df.iloc[-i][col])
                                if col != "Type"
                                else html.Td(
                                    updated_df.iloc[-i][col],
                                    style={"backgroundColor": "green" if updated_df.iloc[-i][
                                                                             "Type"] == "Add" else "orange"},
                                )
                                for col in updated_df.columns
                            ]
                        ) for i in range(5, 0, -1)
                    ],
                    style={'margin': '20px auto', 'width': '70%'}
                ),
            ], style={'textAlign': 'center'}),

            # Updating Inventory Section (unchanged)
            html.Div([
                html.H2("Updating Inventory"),
                html.Label("Select Item"),
                dcc.Dropdown(
                    id="item-dropdown",
                    options=[
                        {'label': 'Strawberry Milk', 'value': 'st_milk'},
                        {'label': 'Chocolate Milk', 'value': 'ch_milk'},
                        {'label': 'Sando', 'value': 'sando'},
                        {'label': 'Biscuit', 'value': 'biscuit'},
                        {'label': 'Chocolate', 'value': 'chocolate'},
                    ],
                    value='st_milk'
                ),
                html.Label("Your Name"),
                dcc.Input(id='name-input', type='text', placeholder='Enter your name'),
                html.Label("Quantity"),
                dcc.Input(id='quantity-input', type='number', placeholder='Enter quantity'),
                html.Button('Add', id='update-button', n_clicks=0),
                html.Div(id='update-result'),
            ], style={'textAlign': 'center'}),

            # New section for plotting inventory over time
            html.Div([
                html.H2("Inventory Trends"),
                dcc.Graph(id='inventory-plot', figure=generate_inventory_plot(updated_df))
            ])
        ], style={'font-family': 'Arial, sans-serif'})

        return updated_layout, ""
    else:
        return dash.no_update, ""


if __name__ == '__main__':
    app.run_server(debug=True)


