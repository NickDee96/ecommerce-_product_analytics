
from datetime import date
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

import re
from flask import Flask, send_from_directory, send_file
import flask

from reviewCrawler import Scraper
from layouts import search_card,get_table,get_rating_row
from nlp import Sentiment
from plots import get_wordcloud,get_starplot,get_dailyplot,get_corrplot

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.MATERIA],
                suppress_callback_exceptions=True)

server = app.server



app.title="Jumia Reviews crawler"

server = app.server
app.layout =dbc.Container([
    dbc.Navbar([
        dbc.Row([
            dbc.Col([
                html.H1(
                    children="Jumia Reviews Crawler",
                    style={
                        "align":"center"
                    }
                )
            ])
        ])
    ]),
    search_card,
    dbc.Spinner(
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Div(id="data_table")
                ],width={"size": 8, "offset": 2})
            ]),
            html.Div(id="rating_row"),
            dbc.Row([
                dbc.Col([
                    dbc.Spinner(
                        html.Div(
                        id="j_vs_sr"
                        )
                    )
                ],width={"size": 8, "offset": 2})
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(id="review_timeseries")
                ])

            ])
        ])

    )

], fluid=True)


@app.callback(
    [Output("download","children"),
    Output("data_table","children"),
    Output("rating_row","children"),
    Output("review_timeseries","children"),],
    [Input("submit","n_clicks")], 
    [State("link_input","value")]
)

def get_data(n_clicks,link):
    if n_clicks:
        print(link)
        X=Scraper(link)
        print(X.status)
        filename=re.sub(r'[^\w\s]','',X.prod_name)
        if X.feed_sect:
            sx=Sentiment(X)
            df=pd.DataFrame(X.rev_list)
            df["Date"]=pd.to_datetime(df.Date,format="%d-%m-%Y").dt.date
            sx.sdf.to_csv(f"output/{filename}_withSentiment.csv",index=False)
            df.to_csv(f"output/{filename}.csv",index=False)
            return [
                    html.Br(),
                    html.A(
                        dbc.Button("Download the csv file", color="primary", className="mr-1",id="download_csv"),
                        href=f"/dash/{filename}.csv"
                    ),
                    html.Br(),
                    html.A(
                        dbc.Button("Download the csv file with Sentiment values", color="primary", className="mr-1",id="download_sent_csv"),
                        href=f"/dash/{filename}_withSentiment.csv"
                    )
                ],[
                html.H3(
                    children=f"Review data for {X.prod_name}"
                ),
                get_table(df)],get_rating_row(X,sx.sdf),[
                    html.Br(),
                    html.H3(
                        "A time series plot of reviews over time"
                    ),
                    dcc.Graph(figure=get_dailyplot(sx.sdf))
                ]
        else:
            return [
                html.Br(),
                html.P(
                    "That product has no reviews at the moment."
                )
            ],[html.Br()],[html.Br()],[html.Br()]
    else:
        return None,None,None,None

@app.server.route('/dash/<filename>') 
def download_csv(filename):
    print(filename)
    value=filename  
    return send_file(f"output/{value}",
                     mimetype='text/csv',
                     attachment_filename=value,
                     as_attachment=True)

if __name__ == "__main__":
    app.run_server(port=5000)