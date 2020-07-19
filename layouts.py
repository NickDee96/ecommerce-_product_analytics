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
                html.Hr(),
                html.Div(id="download")         
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


def get_rating_row(X,sdf):
    return [
        dbc.Row([
            dbc.Col([
                html.H2(
                    children="Jumia Rankings vs Review Sentiment Ranking"
                )
            ],width={"size": 6, "offset": 3})
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(
                            children=("Total Number of Ratings")
                        ),
                        html.H2(
                            children=X.rating_dict['ratings'],
                            style={
                                "color":"black",
                                "display":"inline-block"
                            }                            
                        ),
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(
                            children=("Jumia's average Star rating")
                        ),
                        html.H2(
                            children=round(X.rating_dict['ave_rating'],2),
                            style={
                                "color":"black",
                                "display":"inline-block"
                            }                            
                        ),
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(
                            children=("Total Number of reviews")
                        ),
                        html.H2(
                            children=len(X.rev_list),
                            style={
                                "color":"black",
                                "display":"inline-block"
                            }                            
                        ),
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(
                            children=("Calculated Average Review Sentiment")
                        ),
                        html.H2(
                            children=round(sdf['Combined Sentiment'].mean()*100,2),
                            style={
                                "color":"black",
                                "display":"inline-block"
                            }                            
                        ),
                    ])
                ])
            ])
        ])

    ]   
#def get_wc_plotcard(df,star):
#    card=dbc.Card


