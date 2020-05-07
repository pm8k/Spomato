"""


"""

import os
import pandas as pd
import spotipy
import spotify_token as st


class Spomato(object):

    class validate_token(object):
        def __init__(self, function):
            self._decorated_function = function
        def __call__(self):



            self._decorated_function()


    def __init__(self,
                 username=None,
                 password=None,
                 token_refresh_always=False,
                 token_refresh_time=300):

        self.username = username
        self.password = password
        self.access_token = None
        self.token_expiration_date = None
        self.data = {}
        self.token_refresh_always = token_refresh_always
        self.token_refresh_time = token_refresh_time

        self._get_set_token()
        self._get_spotipy_session()

    def _get_set_token(self):
        if self.username is not None and self.password is not None:
            session_data = st.start_session(self.username,
                                            self.password)
            self.access_token = session_data[0]
            self.token_expiration_date = session_data[1]


    def _get_spotipy_session(self):
        self.spotipy_session = spotipy.Spotify(auth=self.access_token)

    def _parse_album(self, data, market='US'):
        series_list = []
        data = data['tracks']['items']
        # for i in range(len(data)):
        for record in data:
            songid = record['id']
            markets = record['available_markets']
            time = record['duration_ms']/1000
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)
        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])
        return song_df

    def _parse_playlist(self, data, market='US'):
        series_list = []
        data = data['tracks']['items']
        for item in data:
            record = item['track']
            songid = record['id']
            markets = record['available_markets']
            time = record['duration_ms']/1000
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)

        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])

        return song_df

    def _parse_saved_tracks(self, data, market='US'):
        series_list = []
        for item in data:
            record = item['track']
            songid = record['id']
            markets = record['available_markets']
            time = record['duration_ms']/1000
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)
        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])
        return song_df

    def _cache_data(self, data, file_path):
        data.to_csv(file_path, index=False)

    def _load_cached_data(self, file_path):
        data = pd.read_csv(file_path)
        return data

    def get_data(self,
                 current_user_id=None,
                 file_path=None,
                 save=True,
                 source={'savedtracks': None},
                 reset=False,
                 market='US'):
        if file_path:
            if os.path.isfile(file_path) and reset is False:
                data = self._load_cached_data(file_path)
            else:
                data = self._get_new_data(current_user_id=current_user_id,
                                          source=source,
                                          market=market)
                if save:
                    self._cache_data(data=data,
                                     file_path=file_path)

        else:
            data = self._get_new_data(current_user_id=current_user_id,
                                      source=source,
                                      market=market)

        return data

    def _get_new_data(self,
                      current_user_id=None,
                      source={'savedtracks': None},
                      market='US'):
        data_list = []
        for sourcetype in source.keys():
            if sourcetype == 'savedtracks':
                # print 'SAVEDTRACKS'
                data = self._get_saved_tracks()
                data_list.append(data)

            elif sourcetype == 'playlist':
                # print 'PLAYLISTS'
                sourcelist = source[sourcetype]
                playlist_df = self._get_playlists()
                subpdf = playlist_df[playlist_df.playlist_name.isin(sourcelist)]
                playlist_list = []
                for pl_id in subpdf.playlist_id:
                    pl_json = self.spotipy_session.user_playlist(current_user_id, pl_id)
                    pl_df = self._parse_playlist(pl_json)
                    playlist_list.append(pl_df)

                data = pd.concat(playlist_list)
                data.drop_duplicates(inplace=True)
                data_list.append(data)

            elif sourcetype == 'artist':
                # print 'ARTISTS'
                artist_list = []
                for artist in sourcelist:
                    artist_songs = self._get_artist_data(artist)
                    artist_list.append(artist_songs)

                data = pd.concat(artist_list)
                data.drop_duplicates(inplace=True)
                data_list.append(data)

        return data

    def _get_saved_tracks(self):
        end = False
        i = 0
        track_df_list = []
        while not end:
            data = self.spotipy_session.current_user_saved_tracks(limit=50, offset=i*50)['items']
            if len(data) > 0:
                track_df = self._parse_saved_tracks(data)
                track_df_list.append(track_df)
                i += 1
            else:
                end = True


        track_df = pd.concat(track_df_list).reset_index(drop=True)
        track_df.drop_duplicates(inplace=True)

        return track_df

    def pick_tracks(self,
                    track_df,
                    time=25,
                    extra=5,
                    time_limit=None):

        time = time*60
        extra = extra*60
        if time_limit is None:
            time_limit = time/3.0
        track_df = track_df[track_df['time'] <= time_limit]
        time_used = 0

        track_list = []
        done = False
        while not done:

            track_df = track_df[track_df.time <= (time + extra - time_used)]

            if time_used > time:
                done = True

            elif len(track_df).isempty():
                done = True
            else:
                track = track_df.sample().iloc[0]
                track_df = track_df[track_df.song_id != track.song_id]
                track_list.append(track)
                time_used += track.time

        picked_track_df = pd.concat(track_list, axis=1).T

        return picked_track_df



    def _get_artist_data(self, artist_id):
        artist_albums = self.spotipy_session.artist_albums(artist_id)
        album_ids = [x['id'] for x in artist_albums['items']]
        album_jsons = self.spotipy_session.albums(album_ids)['albums']
        songdf = []
        for album in album_jsons:
            songs = self._parse_album(album)
            songdf.append(songs)
        data = pd.concat(songdf)
        return data


    def make_playlist(self,
                      playlist_name,
                      songdf,
                      current_user_id,
                      playlist_df=None):
        if playlist_df is None:
            playlist_df = self._get_playlists()

        if playlist_name in playlist_df.playlist_name.tolist():
            # print('replacing')
            playlist_id = playlist_df[playlist_df.playlist_name == playlist_name].iloc[0].playlist_id
            self.spotipy_session.user_playlist_replace_tracks(user=current_user_id,
                                                              playlist_id=playlist_id,
                                                              tracks=songdf.song_id.tolist()
                                                             )
        else:
            # print('new!')
            self.spotipy_session.user_playlist_create(current_user_id,
                                                      playlist_name,
                                                      public=False)
            playlist_df = self._get_playlists()
            playlist_id = playlist_df[playlist_df.playlist_name == playlist_name].iloc[0].playlist_id
            self.spotipy_session.user_playlist_add_tracks(current_user_id,
                                                          playlist_id,
                                                          tracks=songdf.song_id.tolist()
                                                         )


    def artist_id_search(self,
                         artist,
                         limit=10,
                         offset=0):
        artist_results = self.spotipy_session.search(artist,
                                                     type='artist',
                                                     limit=limit,
                                                     offset=offset)
        artist_items = artist_results['artists']['items']

        if len(artist_items) > 0:
            index = ['artist', 'id']
            artist_df = pd.concat([pd.Series([x['name'], x['id']], index=index) for x in artist_items], axis=1).T
        else:
            artist_df = pd.DataFrame(columns=['name', 'id'])
        return artist_df

    def _get_playlists(self):
        pl_json = self.spotipy_session.current_user_playlists()
        playlist_list = [pd.Series([pl['name'], pl['id']], index=['playlist_name', 'playlist_id']) for pl in pl_json['items']]
        playlist_df = pd.concat(playlist_list, axis=1).T
        return playlist_df
