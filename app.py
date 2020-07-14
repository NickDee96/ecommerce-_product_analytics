
from datetime import date
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory, send_file
import flask

from reviewCrawler import Scraper
from layouts import search_card
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.MATERIA],
                server=flask.Flask('app'),
                suppress_callback_exceptions=True)

server = app.server



app.title="Jumia Reviews crawler"

server = app.server
app.layout =dbc.Container([
    dbc.Navbar([
        dbc.Row([
            dbc.Col(
                html.H1(
                    children="Jumia Reviews Crawler"
                )
            )
        ])
    ]),
    search_card,
    dbc.Row([
        dbc.Col([
            html.Div(id="download")
        ],width={"size": 6, "offset": 3})
    ])
], fluid=True)


@app.callback(
    Output("download","children"),
    [Input("submit","n_clicks")], 
    [State("link_input","value")]
)

def get_data(n_clicks,link):
    if n_clicks:
        print(link)
        X=Scraper(link)
        print(X.status)
        if X.feed_sect:
            pd.DataFrame(X.rev_list).to_csv(f"output/{X.sku}.csv",index=False)
            return [
                    html.Br(),
                    html.A(
                        dbc.Button("Download the csv file", color="primary", className="mr-1",id="download_csv"),
                        href=f"/dash/{X.sku}.csv"
                )
            ]
        else:
            return [
                html.Br(),
                html.P(
                    "That product has no reviews at the moment."
                )
            ]

@app.server.route('/dash/<filename>') 
def download_csv(filename):
    #value = flask.request.args.get('value')
    print(filename)
    value=filename
    # create a dynamic csv or file here using `StringIO` 
    # (instead of writing to the file system)
    #strIO = StringIO.StringIO()
    #strIO.write('You have selected {}'.format(value)) 
    #strIO.seek(0)    
    return send_file(f"output/{value}",
                     mimetype='text/csv',
                     attachment_filename=value,
                     as_attachment=True)

if __name__ == "__main__":
    app.run_server(debug=True)