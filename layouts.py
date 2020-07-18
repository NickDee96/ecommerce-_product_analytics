import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash_table import DataTable

search_card=dbc.Row([
    dbc.Col([
        html.Br(),
        html.Br(),
        dbc.Card([
            dbc.CardBody([
                html.H3(
                    children="Enter the Jumia product link in the box below and click submit to crawl its reviews"
                ),
                dbc.Input(
                    placeholder = "Insert link here",
                    bs_size="md",
                    className="mb-3",
                    id = "link_input"
                ),
                html.Br(),
                dbc.Button("Submit", color="primary", className="mr-1",id="submit"),         
            ])
        ])
    ],width={"size": 6, "offset": 3})
])


def get_table(df):
    return DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                    'textAlign': 'left',
                    'fontSize':15,
                    'font-family':'roboto'
                },
                style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                sort_action='native',
                page_size=10
            )


