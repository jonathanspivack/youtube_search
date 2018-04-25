#!/usr/bin/env python3
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import defaultdict
import datetime
from cap_dictionary import captionsd, lasttimestamp
from urllib.parse import urlparse
from urllib.parse import parse_qs
# from dash.dependencies import Input, Output

## Clean strings of times and turn them into datetime objects
def searchword_cleanlasttime(strword, timestamp):
    stringtimes=captionsd[strword.lower()]
    print ("******dictionary values*****  ", stringtimes)
    datetimeL=[]
    for stringy in stringtimes:
        conversion= stringy.split(':')
        minz=int(conversion[0])
        secondz=int(conversion[1])
        if minz>59:
            newmins=minz-60
            timeobj=datetime.time(1, newmins, secondz)
        else:
            timeobj=datetime.time(0, minz, secondz)
        datetimeL.append(timeobj)

    ## Cleaning the last time stamp now + 2 minutes at the end
    lastty=timestamp.split(':')
    lastmin=int(lastty[0])
    lastsec=int(lastty[1])
    if lastmin>59:
        newminz=lastmin-60
        lastobj=datetime.datetime(2000,1,1,1, newminz+2, lastsec)
    else:
        lastobj=datetime.datetime(2000,1,1,0, lastmin+2, lastsec)
    return(strword, datetimeL, lastobj)

def makeintervals(interval_length, maxtime):
    intervalm=int(interval_length)
    starttime=datetime.datetime(2000,1,1,0,0,0)
    running=starttime
    intervallist=[]
    while running <maxtime:
        running+=datetime.timedelta(minutes=intervalm)
        intervallist.append(running.time())
    return intervalm,intervallist


def classify_times(list_of_intervals, list_of_timestamps):
    countfreq=defaultdict(int)
    rawtimes=defaultdict(list)
    for timeinterval in list_of_intervals:
        strinterval=timeinterval.strftime('%H:%M:%S')
        countfreq[strinterval]=0
        rawtimes[strinterval]
    for ourtime in list_of_timestamps:
        for i in range (-1, len(list_of_intervals)):
            if i+1 == 0:
                if ourtime <= list_of_intervals[i+1]:
                    strinterval=list_of_intervals[i+1].strftime('%H:%M:%S')
                    rawtimes[strinterval].append(ourtime.strftime('%H:%M:%S'))
                    countfreq[strinterval]+=1
                    break
            else:
                if ourtime >= list_of_intervals[i] and  ourtime <= list_of_intervals[i+1]:
                    strinterval=list_of_intervals[i+1].strftime('%H:%M:%S')
                    rawtimes[strinterval].append(ourtime.strftime('%H:%M:%S'))
                    countfreq[strinterval]+=1
                    break
    print ("Each interval's raw time stamps:" ,rawtimes)
    print("Each interval's frequency: ", countfreq)
    return(rawtimes, countfreq)


def make_x_y_values(dict_raw_times, dict_count_freq):
    xaxis=[key for key in sorted(list(dict_count_freq.keys()))]
    yaxis=[value for key,value in sorted(list(dict_count_freq.items()))]
    rawtimestamps= [str(value) for key,value in sorted(list(dict_raw_times.items()))]
    return(xaxis, yaxis, rawtimestamps)


def makelist_timestamps(times_dictionary):
    listoftimes=[]
    for key in times_dictionary.keys():
        for timestamp in times_dictionary[key]:
            listoftimes.append(timestamp)
    sortedtimes=sorted(listoftimes)
    finaltimestamps=[]
    for eachtime in sortedtimes:
            finaltimestamps.append(html.Div(children="""{time}""".format(time=eachtime)))
    # listoftimes.append(style={'width':'180', 'height':'200', 'overflow':'scroll'})
    return finaltimestamps

def make_time_buckets():
    befor_keyowrd, keyword, after_keyword = lasttimestamp.partition(":")
    lasttimestamp_num = int(befor_keyowrd)
    if lasttimestamp_num < 10:
        return int(lasttimestamp_num/1)
    elif lasttimestamp_num < 30:
        return int(lasttimestamp_num / 5)
    else:
        return int(lasttimestamp_num / 10)

YOUTUBE_DOMAINS = [
    'youtu.be',
    'youtube.com',
]

def extract_id(yt_url_string):
    # Make sure all URLs start with a valid scheme
    if not yt_url_string.lower().startswith('http'):
        yt_url_string = 'http://{}'.format(yt_url_string)

    yt_url = urlparse(yt_url_string)

    # Check host against whitelist of domains
    if yt_url.hostname.replace('www.', '') not in YOUTUBE_DOMAINS:
        return None

    # Video ID is usually to be found in 'v' query string
    qs = parse_qs(yt_url.query)
    if 'v' in qs:
        yt_id=qs['v'][0]
        embed_url = "https://www.youtube.com/embed/" + yt_id

        return embed_url

    if 'embed' in yt_url.path:
        return yt_url_string
    # Otherwise fall back to path component
    yt_id=yt_url.path.lstrip('/')
    embed_url = "https://www.youtube.com/embed/" + yt_id
    return embed_url




    # if lasttimestamp_num < 10:
    #     return 1
    # elif lasttimestamp_num < 30:
    #     return 5
    # else:
    #     return 10






## Dash app ##
# def make_dash_app_graph(searchedword, intervalm, xaxis, yaxis, rawtimestamps):
#     app=dash.Dash()
#     data=[go.Bar(x=xaxis, y=yaxis, name='{}'.format(searchedword), text=rawtimestamps,
#                              marker=dict(color='rgb(78, 150, 150)'), hoverinfo='all')]
#     layout=go.Layout(
#         title='Frequency for word = " {word}" in intervals of {min} minutes '.format(word=searchedword, min=intervalm),
#         xaxis=dict(title='Timestamp in video'),
#         yaxis=dict(title='Occurrence frequency of word',autotick=True ),
#         bargap=0.1
#
#         )
#
#     app.layout = html.Div(children=[
#         html.H1(children='YouTUbe '),
#         dcc.Graph(
#             id='freqchart',
#             figure=go.Figure(
#                 data=data,
#                 layout=layout )
#                 )])
#     return app



# if __name__ == '__main__':
#     # targetword=str(input("Input your word: ")).lower()
#     # interval_min=int(input("Input your interval length in minutes: "))
#     # searchedword, list_times, lasttime= searchword_cleanlasttime(targetword, lasttimestamp)
#     # intervalm, listofintervals=makeintervals(interval_min, lasttime)
#
#     ## Hardcoded search word and time interval:
#     searchedword, list_times, lasttime= searchword_cleanlasttime("youtube", lasttimestamp)
#     intervalm, listofintervals=makeintervals(20, lasttime)
#
#     dict_raw_times, dict_count_freq= classify_times(listofintervals, list_times)
#     xaxis, yaxis, rawtimestamps= make_x_y_values(dict_raw_times, dict_count_freq)
#
#     app= make_dash_app_graph(searchedword, intervalm, xaxis, yaxis, rawtimestamps)
#
#     #app.run_server(debug=True)