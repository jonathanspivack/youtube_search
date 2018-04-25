# !/usr/bin/env python3
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from cap_dictionary import captionsd, lasttimestamp
from dash.dependencies import Input, Output
from data_cleaning import searchword_cleanlasttime as searchword_cleanlasttime
from data_cleaning import makeintervals as makeintervals
from data_cleaning import classify_times as classify_times
from data_cleaning import make_x_y_values as make_x_y_values
from data_cleaning import makelist_timestamps as makelist_timestamps
from crawl import pull_transcript as pull_transcript
from data_cleaning import make_time_buckets as make_time_buckets
from data_cleaning import extract_id
from cacher import search_cache
import time


app = dash.Dash()

# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.css.append_css({'external_url': 'https://codepen.io/ivyjx/pen/deGQGd.css'})

# app.layout = html.Div(children=[
#
#     html.Div(id='target'),
#     html.Div(children='''
#         Search a youtube video:
#     '''),
#     dcc.Input(id='input_url', value='', type='text'),
#
#     html.Div(children='''
#         Word to graph:
#     '''),
#     dcc.Input(id='input', value='', type='text'),
#     html.Div(id='output-graph'),
#
# ])


app.layout = html.Div(children=[
    html.H1(children='YouTube Suite', style={
        'textAlign': 'center', }),
    html.P(children='Application to search the content of a YouTube video', style={
        'textAlign': 'center', }),
    html.Div([
        html.Div([
            html.Div(children='''
                        Search a YouTube video:
                    '''),
            dcc.Input(
                id='input_url',
                placeholder='Enter video link...',
                type='text',
                size=85,
                value='',
            ),
        ], className='eight columns')
        ,

        html.Div([
            html.Div(children='''
                        Search a word:
                    '''),
            dcc.Input(
                id='input',
                placeholder='Enter a word to search...',
                type='text',
                size=20,
                value='', ),

        ], className='four columns'),

    ], className='row', style={'margin-top': '20'}),

    html.Div([

            html.Div(
                    [
        html.Div(
            [
                html.Div(id='target'),
            ],
                    className='video-container'    ),
        ],
            className='eight columns',
            style={'margin-top': '20'}
        ),
        html.Div(
            [
                # html.H4('Timestamps',),
                html.Div(id='timestamplist'),
                # html.Div(
                # # listtimes, #FIXME
                # style={'width':'180', 'height':'200', 'overflow':'scroll'}   ),
            ], className='four columns', style={'margin-top': '20'}),
    ], className='row'),

    html.Div([
        html.Div(id='output-graph',
                 className='twelve columns', ),
    ], className='row'),

# html.A(
#         'Download Yo Captions',
#         id='download-link',
#         download="youtube_captions.csv",
#         href="src/youtube_captions.csv",
#         target="_blank"
#     )


],
    className='ten columns offset-by-one', style={'display': 'inline-block'})


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    try:
        from cap_dictionary import captionsd, lasttimestamp
        searchedword, list_times, lasttime = searchword_cleanlasttime(input_data, lasttimestamp)
        buckets = make_time_buckets()
        intervalm, listofintervals = makeintervals(buckets, lasttime)
        dict_raw_times, dict_count_freq = classify_times(listofintervals, list_times)

        xaxis, yaxis, rawtimestamps = make_x_y_values(dict_raw_times, dict_count_freq)
        data = [go.Bar(x=xaxis, y=yaxis, name='{}'.format(searchedword), text=rawtimestamps,
                       marker=dict(color='rgb(78, 150, 150)'), hoverinfo='all')]

        layout = go.Layout(
            title='Frequency for word = " {word}" in intervals of {min} minutes '.format(word=searchedword,
                                                                                         min=intervalm),
            xaxis=dict(title='Timestamp in video'),
            yaxis=dict(title='Occurrence frequency of word', autotick=True),
            bargap=0.1

        )

        return dcc.Graph(
            id='freqchart',
            figure=go.Figure(
                data=data,
                layout=layout)
        )


    except:
        #return "That word is not in the video!"
        return " "


@app.callback(Output('target', 'children'), [Input(component_id='input_url', component_property='value')])
def embed_iframe(value):
    # raw url to embed url
    # befor_keyowrd, keyword, after_keyword = value.partition("=")
    # embed_url = "https://www.youtube.com/embed/" + after_keyword
    # print(value)
    watchlink = str(value)
    cache_lasttimestamp, cache_captionsd  = search_cache(value)
    if cache_lasttimestamp == False and cache_captionsd == False:
        pull_transcript(watchlink)
    else:
        lasttimestamp = cache_lasttimestamp
        captionsd = cache_captionsd
        with open('cap_dictionary.py', 'w') as medict:
            medict.write("#!/usr/bin/env python3\n\n")
            medict.write("lasttimestamp=\"{}\"\n\n".format(lasttimestamp))
            medict.write("captionsd={}\n\n".format(captionsd))

    embed_url = extract_id(value)
    print(embed_url)

    return html.Iframe(src=embed_url, width='560', height='315', )



# https://www.youtube.com/watch?v=sh-MQboWJug
# https://www.youtube.com/embed/sh-MQboWJug
# https://www.youtube.com/embed/uZs1AHQBz24?rel=0
# https://www.youtube.com/watch?v=NAp-BIXzpGA&pbjreload=10
# https://www.youtube.com/embed/NAp-BIXzpGA




@app.callback(Output(component_id='timestamplist', component_property='children'),
              [Input(component_id='input', component_property='value')]
              )
def listingtimes(input_data):
    try:
        from cap_dictionary import captionsd, lasttimestamp
        searchedword, list_times, lasttime = searchword_cleanlasttime(input_data, lasttimestamp)
        intervalm, listofintervals = makeintervals(10, lasttime)
        dict_raw_times, dict_count_freq = classify_times(listofintervals, list_times)
        listtimes = makelist_timestamps(dict_raw_times)
        return html.Div(listtimes, style={'width': '180', 'height': '200', 'overflow': 'scroll'}, )

    except:
        return ""


if __name__ == '__main__':
    app.run_server(port=8553, debug=True)
