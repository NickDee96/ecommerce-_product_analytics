import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
                dbc.Button("Submit", color="primary", className="mr-1",id="submit")                
            ])
        ])
    ],width={"size": 6, "offset": 3})
])

