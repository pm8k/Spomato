import pandas as pd

def parse_album(data, market='US'):
    series_list = []
    data = data['tracks']['items']
    for i in range(len(data)):
        record = data[i]
        songid = record['id']
        markets = record['available_markets']
        time = record['duration_ms']/1000
        if market in markets:
            series = pd.Series([songid,time],index=['song_id','time'])
            series_list.append(series)
    if len(series_list)>0:
        df = pd.concat(series_list,axis=1).transpose()
    else:
        df = pd.DataFrame(columns=['song_id','time'])
    return df

def parse_playlist(data, market='US'):
    series_list = []
    data = data['tracks']['items']
    for i in range(len(data)):
        record = data[i]['track']
        songid = record['id']
        markets = record['available_markets']
        time = record['duration_ms']/1000
        if market in markets:
            series = pd.Series([songid,time],index=['song_id','time'])
            series_list.append(series)

    df = pd.concat(series_list,axis=1).transpose()

    return df

def parse_saved_tracks(data,market='US'):
    series_list = []
    for i in range(len(data)):
        record = data[i]['track']
        songid = record['id']
        markets = record['available_markets']
        time = record['duration_ms']/1000
        if market in markets:
            series = pd.Series([songid,time],index=['song_id','time'])
            series_list.append(series)

    df = pd.concat(series_list,axis=1).transpose()

    return df
