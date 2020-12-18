# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

import plotly.graph_objs as go



def get_options(list_counties):
    dict_list = []
    for i in list_counties:
        dict_list.append({'label':i, 'value':i})
    return dict_list


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.read_csv('diag_norm.csv')


app.layout = html.Div(children=[
    html.H1(children='Michigan Covid 19'),

    html.Div(children='''
        Current - view of Postive & Negative cases in Michigan.
    '''),

    dcc.Graph(
        id='positive-graph',
        figure = {}
    ),
    dcc.Graph(
        id='negative-graph',
        figure = {}
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(id = 'County-drop',
        options=get_options(df['County'].unique()),
        value=['Michigan'],
        multi=True
    ),


    
])


@app.callback([
    Output('positive-graph', 'figure'),
    Output('negative-graph', 'figure')],
    [Input('County-drop', 'value')]
)
def update_figure(selected_county):
    print(selected_county)
    df_sub = pd.DataFrame()

    for county in selected_county:
        df_sub = df_sub.append(df[df['County']==county])
    print(df_sub.head())
    trace = []
    #df_sub = df

    trace_2 = px.line(df_sub, x="MessageDate", y=["Positive", "Negative"], color = 'County')
    trace_3 = px.line(df_sub, x="MessageDate", y="Negative", color = 'County')
    #fig = go.Figure(data=[trace_2], layout = layout)
    #fig.add_trace(trace_2)
    #fig.add_trace(trace_3)

    return trace_2, trace_3

if __name__ == '__main__':
    app.run_server(debug=True)