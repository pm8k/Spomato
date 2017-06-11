
import os
import pandas as pd
from spomato.parsers import parse_album, parse_playlist, parse_saved_tracks

file_path = os.path.expanduser('~')+'/'

def cache_data(data,profile):
    data.to_csv(file_path+profile,index=False)

def load_cached_data(profile):
    data = pd.read_csv(file_path+profile)
    return data

def get_data(current_user_id=None,sp=None,profile_name=None,save=True,sourcetype='savedtracks',sourcelist=[],reset=False):
    if profile_name:
        if os.path.isfile(file_path+profile_name) and reset==False:
            data = load_cached_data(profile_name)
            # print 'loading from csv'
        else:
            data = get_new_data(current_user_id=current_user_id,sp=sp,sourcetype=sourcetype,sourcelist=sourcelist)
            # print 'loading data under profile'
            if save:
                cache_data(data,profile_name)
                # print 'caching data'

    else:

        data = get_new_data(current_user_id=current_user_id,sp=sp,sourcetype=sourcetype,sourcelist=sourcelist)
        # print 'just getting data'

    return data

def get_new_data(current_user_id,sp=None,sourcetype='savedtracks',sourcelist=[], market='US'):

    if sourcetype == 'savedtracks':
        # print 'SAVEDTRACKS'
        data = get_saved_tracks(sp)

    elif sourcetype == 'playlist':
        # print 'PLAYLISTS'
        playlist_df = get_playlists(sp)
        subpdf = playlist_df[playlist_df.playlist_name.isin(sourcelist)]
        dflist=[]
        for pl_id in subpdf.playlist_id:
            pl_json=sp.user_playlist(current_user_id,pl_id)
            pl_df = parse_playlist(pl_json)
            dflist.append(pl_df)

        data = pd.concat(dflist)
        data.drop_duplicates(inplace=True)

    elif sourcetype == 'artist':
        # print 'ARTISTS'
        dflist=[]
        for artist in sourcelist:
            artist_songs = get_artist_data(sp,artist)
            dflist.append(artist_songs)

        data = pd.concat(dflist)
        data.drop_duplicates(inplace=True)

    return data

def get_saved_tracks(read_sp):
    end=False
    i=0
    dflist = []
    while not end:
        data = read_sp.current_user_saved_tracks(limit=50,offset=i*50)['items']
        if len(data)>0:
            df = parse_saved_tracks(data)
            dflist.append(df)
            i+=1
        else:
            end=True


    df = pd.concat(dflist).reset_index(drop=True)

    return df

def pick_songs(df, time=25, extra=5, time_limit=None):

    time = time*60
    extra = extra*60
    if time_limit == None:
        time_limit = time/3.0
    subdf = df[df.time<=time_limit]
    time_used = 0

    song_list = []
    done = False
    while not done:

        subdf2 = subdf[subdf.time<=(time+extra-time_used)]

        if time_used > time:
            done = True

        elif len(subdf2)==0:
            done=True
        else:
            song = subdf2.sample().iloc[0]
            df = df[df.song_id!=song.song_id]
            subdf = subdf[subdf.song_id!=song.song_id]

            song_list.append(song)
            time_used += song.time

    songdf = pd.concat(song_list,axis=1).T

    return songdf, df



def get_artist_data(sp,artist_id):
    artist_albums=sp.artist_albums(artist_id)
    album_ids = [x['id'] for x in artist_albums['items']]
    album_jsons = sp.albums(album_ids)['albums']
    songdf = []
    for album in album_jsons:
        songs=parse_album(album)
        songdf.append(songs)
    data = pd.concat(songdf)
    return data


def make_playlist(sp, playlist_name,songdf,current_user_id,playlist_df=None):
    if playlist_df==None:
        playlist_df = get_playlists(sp)

    if playlist_name in playlist_df.playlist_name.tolist():
        # print('replacing')
        playlist_id = playlist_df[playlist_df.playlist_name==playlist_name].iloc[0].playlist_id
        sp.user_playlist_replace_tracks(user = current_user_id,
                                            playlist_id = playlist_id,
                                            tracks = songdf.song_id.tolist()
                                           )
    else:
        # print('new!')
        sp.user_playlist_create(current_user_id, playlist_name, public=False)
        playlist_df = get_playlists(sp)
        playlist_id = playlist_df[playlist_df.playlist_name==playlist_name].iloc[0].playlist_id
        sp.user_playlist_add_tracks(current_user_id,playlist_id,tracks = songdf.song_id.tolist())


def artist_id_search(sp, artist,limit=10,offset=0):
    ooo=sp.search(artist,type='artist',limit=limit,offset=offset)['artists']['items']

    if len(ooo)>0:
        index=['artist','id']
        df = pd.concat([pd.Series([x['name'],x['id']],index=index) for x in ooo],axis=1).T
    else:
        df=pd.DataFrame(columns=['name','id'])
    return df

def get_playlists(mod_sp):
    pl_json = mod_sp.current_user_playlists()
    playlist_list = [pd.Series([pl['name'],pl['id']],index=['playlist_name','playlist_id']) for pl in pl_json['items']]
    playlist_df = pd.concat(playlist_list,axis=1).T
    return playlist_df
