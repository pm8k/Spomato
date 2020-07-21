"""Author: Matthew Russell

This contains the main Spomato class to be used to access the Spotify API and create new playlists based on the user's
defined criteria.

"""

import os
import pandas as pd
import spotipy

class Spomato():
    """Object used to access spotify API through spotipy and generate playlists.

    This can take a combination user's saved tracks, playlists, and/or artist's songs to generate a playlist of a
    specified length. This was conceived to use the Tomato Timer method as Spotify playlists.

    This does require the user to provide a user API token from the spotify API. The API scopes used by this library are
    playlist-read-private, playlist-modify-private, and user-library-read.

    Parameters
    ----------
    access_token : str
        A valid Spotify Access token.

    Attributes
    ----------
    data : dictionary
        Dictionary storing available data structures to create playlists.
    spotipy_session : spotipy.client.Spotify
        A spotipy session to access the spotify API.
    access_token : str
        A valid Spotify Access token. This requires the scopes playlist-read-private, playlist-modify-private,
        and user-library-read
    current_user_id : str
        The string id of the user of the access token used to create the spotipy session.

    """

    def __init__(self,
                 access_token=None):
        """Initialization function that sets access token and generates initial spotipy session.

        Parameters
        ----------
        access_token : str
            A valid Spotify Access token. This requires the scopes playlist-read-private, playlist-modify-private,
            and user-library-read.

        Returns
        -------
        None

        """

        self.access_token = access_token
        self.data = {}
        self.spotipy_session = self._get_spotipy_session()
        self.current_user_id = self.spotipy_session.current_user()['id']


    def update_token(self, access_token):
        """Updates the token and spotify session with the provided access_token. Generally used if your access token
        has expired.

        Parameters
        ----------
        access_token : str
            A valid Spotify Access token. This requires the scopes playlist-read-private, playlist-modify-private,
            and user-library-read.

        Returns
        -------
        None

        """
        # update the class access token and the spotipy session
        self.access_token = access_token
        self.spotipy_session = self._get_spotipy_session()
        self.current_user_id = self.spotipy_session.current_user()['id']


    def _get_spotipy_session(self):
        """Internal Function to create a new spotify session.

        Returns
        -------
        spotipy_session : spotipy.client.Spotify
            A spotipy session to access the spotify API.

        """
        return spotipy.Spotify(auth=self.access_token)


    @staticmethod
    def _parse_album(album_data, market='US'):
        """Parses the album data returned from the Spotify API and returns the song information as a pandas DataFrame.

        Parameters
        ----------
        album_data : dict
            A dictionary of album data from Spotify API
        market : str
            A string representation of the Spotify market to filter on. Default is 'US'

        Returns
        -------
        pandas.DataFrame
            A dataframe of song ids and time for each song

        """
        # iterate over each record in the album data and parse the track data
        series_list = []
        album_tracks = album_data['tracks']['items']
        for record in album_tracks:
            songid = record['id']
            markets = record['available_markets']
            # time is stored in milliseconds, divide to convert to seconds.
            time = record['duration_ms']/1000
            # filter out any songs that are not in the specified market
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)
        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])
        return song_df

    @staticmethod
    def _parse_user_playlist(data, market='US'):
        """Parses a user playlist data set from the Spotify API and returns the song information as a pandas DataFrame.

        Parameters
        ----------
        data : dictionary
            Contains songs in a playlist from the Spotify API
        market : str
            A string representation of the Spotify market to filter on. Default is 'US'

        Returns
        -------
        pandas.DataFrame
            A dataframe of song ids and time for each song

        """
        # iterate over each record in the playlist data and parse the track data
        series_list = []
        data = data['tracks']['items']
        for item in data:
            record = item['track']
            songid = record['id']
            markets = record['available_markets']
            # time is stored in milliseconds, divide to convert to seconds.
            time = record['duration_ms']/1000
            # filter out any songs that are not in the specified market
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)

        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])

        return song_df


    @staticmethod
    def _parse_public_playlist(data, market='US'):
        """Parses public playlist data set from the Spotify API and returns the song information as a pandas DataFrame.

        Parameters
        ----------
        data : dictionary
            Contains songs in a playlist from the Spotify API
        market : str
            A string representation of the Spotify market to filter on. Default is 'US'

        Returns
        -------
        pandas.DataFrame
            A dataframe of song ids and time for each song

        """
        # iterate over each record in the playlist data and parse the track data
        series_list = []
        data = data['items']
        for item in data:
            record = item['track']
            songid = record['id']
            markets = record['available_markets']
            # time is stored in milliseconds, divide to convert to seconds.
            time = record['duration_ms']/1000
            # filter out any songs that are not in the specified market
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)

        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])

        return song_df


    @staticmethod
    def _parse_saved_tracks(data, market='US'):
        """Parses a the saved songs data set of the user from the Spotify API and returns the song information as a
        pandas DataFrame.

        Parameters
        ----------
        data : dictionary
            Contains saved songs of the user from the Spotify API
        market : str
            A string representation of the Spotify market to filter on. Default is 'US'

        Returns
        -------
        pandas.DataFrame
            A dataframe of song ids and time for each song

        """
        # iterate over each record in the saved track data and parse the individual track data
        series_list = []
        for item in data:
            record = item['track']
            songid = record['id']
            markets = record['available_markets']
            # time is stored in milliseconds, divide to convert to seconds.
            time = record['duration_ms']/1000
            # filter out any songs that are not in the specified market
            if market in markets:
                series = pd.Series([songid, time], index=['song_id', 'time'])
                series_list.append(series)
        if len(series_list) > 0:
            song_df = pd.concat(series_list, axis=1).transpose()
        else:
            song_df = pd.DataFrame(columns=['song_id', 'time'])
        return song_df


    def _cache_data(self, data_key, file_path):
        """Export the results of a dataset of song ids to local filesystem as a csv.

        Parameters
        ----------
        data_key : str
            Key of the dataset to save
        file_path : str
            Full path of filename to save the file.

        Returns
        -------
        None

        """
        # use pandas dataframe write function to save file
        self.data[data_key].to_csv(file_path, index=False)


    def _load_cached_data(self, data_key, file_path):
        """Load a Saved Dataset into the Spomato data dictionary. Requires a csv with columns of 'song_id' and 'time'.

        Parameters
        ----------
        data_key : str
            Key to associate the loaded dataset in the data dictionary.
        file_path : str
            Full path of filename to load the file.

        Returns
        -------
        None

        """
        data = pd.read_csv(file_path)

        # ensure the required columns are in the dataset else raise error
        if 'song_id' not in data.columns:
            raise ValueError('Column song_id not found in loaded data file.')
        if 'time' not in data.columns:
            raise ValueError('Column song_id not found in loaded data file.')

        # data looks correct, add dataset to data
        self.data[data_key] = data


    def get_file_data(self,
                      data_key='default',
                      file_path=None,
                      overwrite=False):
        """Loads a file of song data into Spomato to be used for generating new playlists.

        Parameters
        ----------
        data_key : str
            Key to associate the dataset in the data dictionary.
        file_path : str
            Full path of filename if loading or saving dataset.
        overwrite : bool
            Boolean to determine if the dataset should be overwritten if it already exists.


        Returns
        -------
        None

        """
        if not isinstance(data_key, str):
            raise TypeError('Argument data_key must be of type string')
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError('Argument file_path must be of type string')
        # check if the data key already exists to ensure data is not unexpectedly overwritten
        if data_key in self.data.keys() and overwrite is False:
            msg = (f'Dataset {data_key} already exists and reset argument is set to False. '
                   'Set reset to True to overwrite dataset.')
            raise ValueError(msg)

        # read the data from file if the file exists
        if os.path.isfile(file_path):
            self._load_cached_data(data_key=data_key,
                                   file_path=file_path)
        else:
            raise ValueError('File path {f} does not exist.'.format(f=file_path))


    def get_api_data(self,
                     data_key='default',
                     file_path=None,
                     source=None,
                     reset=False,
                     market='US'):
        """Generates a song dataset to load into Spomato to be used for generating new playlists.


        Parameters
        ----------
        data_key : str
            Key to associate the dataset in the data dictionary.
        file_path : str
            If not None, the dataset generated will also be saved to the specified file path..
        source : dict
            Contains all sources you want to use in generating the dataset. The dictionary is keyed by one of 3 source
            types: savedtracks, playlist, or artist. For savedtracks the value can be None, as no further data is
            required. For playlist or artist, the value should contain a list of all spotify ids of the appropriate
            type. If not specified, it defaults to your saved tracks.
        reset : bool
            Boolean to determine if the dataset should be regenerated if it already exists.
        market : str
            A string representation of the Spotify market to filter on. Default is 'US'

        Returns
        -------
        None

        """
        if not isinstance(data_key, str):
            raise TypeError('Argument data_key must be of type string')
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError('Argument file_path must be of type string')
        if source is not None and not isinstance(source, dict):
            raise TypeError('Argument source must be of type dict')
        if not isinstance(reset, (bool, int)):
            raise TypeError('Argument reset must be of type bool or int')
        if not isinstance(market, str):
            raise TypeError('Argument market must be of type string')
        # check if the data key already exists to ensure data is not unexpectedly overwritten
        if data_key in self.data.keys() and reset is False:
            msg = (f'Dataset {data_key} already exists and reset argument is set to False. '
                   'Set reset to True to overwrite dataset.')
            raise ValueError(msg)

        # default the data source to the user's saved tracks if not specified
        if source is None:
            source = {'savedtracks': None}

        # generate the dataset and save it into the Spomato object
        self.data[data_key] = self._get_new_data(source=source,
                                                 market=market)

        # Cache the data if the file_path is specified
        if file_path:
            self._cache_data(data_key=data_key,
                             file_path=file_path)


    def _get_playlist_dataframe(self,
                                source_list,
                                market):
        """Short summary.

        Parameters
        ----------
        source_list : list
            A list of playlist ids to source songs from
        market : str
            A string representation of the Spotify market to filter on.

        Returns
        -------
        pandas.DataFrame
            A dataframe of songs with song id and time.

        """
        # get the list of playlists and filter out datasets included in the source list
        playlist_df = self.get_playlists()

        playlist_list = []
        for pl_id in source_list:
            if not playlist_df[playlist_df.playlist_id == pl_id].empty:
                pl_json = self.spotipy_session.user_playlist(self.current_user_id, pl_id)
                pl_df = self._parse_user_playlist(pl_json, market)
                playlist_list.append(pl_df)
            else:
                pl_json = self.spotipy_session.playlist_tracks(pl_id)
                pl_df = self._parse_public_playlist(pl_json, market)
                playlist_list.append(pl_df)

        if len(playlist_list) == 0:
            raise ValueError('No valid playlists.')

        # concatinate the dataframes of all the playlist and remove any duplicates
        data = pd.concat(playlist_list)
        data.drop_duplicates(inplace=True)

        return data


    def _get_artist_dataframe(self,
                              source_list,
                              market):
        """Short summary.

        Parameters
        ----------
        source_list : list
            A list of playlist ids to source songs from
        market : str
            A string representation of the Spotify market to filter on.

        Returns
        -------
        pandas.DataFrame
            A dataframe of songs with song id and time.

        """
        # iterate over each artist, get the data from the Spotify API, and parse the song data
        artist_list = []
        for artist in source_list:
            artist_songs = self._get_artist_data(artist, market)
            artist_list.append(artist_songs)

        # concatinate the dataframes of all the playlist and remove any duplicates
        data = pd.concat(artist_list)
        data.drop_duplicates(inplace=True)

        return data


    def _get_new_data(self,
                      source=None,
                      market='US'):
        """Creates a new dataset from the specified source list and returns a pandas DataFrame of song ids and times.

        Parameters
        ----------
        source : dict
            Contains all sources you want to use in generating the dataset. The dictionary is keyed by one of 3 source
            types: savedtracks, playlist, or artist. For savedtracks the value can be None, as no further data is
            required. For playlist or artist, the value should contain a list of all spotify ids of the appropriate
            type.
        market : str
            A string representation of the Spotify market to filter on.

        Returns
        -------
        pd.DataFrame
            A dataframe of song ids generated from the sources.

        """
        # if the source is not specified, default to the saved tracks of the current user.
        if source is None:
            source = {'savedtracks': None}
        elif not isinstance(source, dict):
            raise ValueError('Argument source must be of type dict or None.')
        elif len(source.keys()) == 0:
            raise ValueError('Argument source must contain at least 1 valid key from: savedtracks, artist, playlist')
        else:
            for key in source.keys():
                if key not in ['savedtracks', 'artist', 'playlist']:
                    raise ValueError(f'{key} is not a valid data source type.')

        # iterate over the source types in the source dictionary and parse out the data
        data_list = []
        for sourcetype in source.keys():
            if sourcetype == 'savedtracks':
                # print 'SAVEDTRACKS'
                data = self._get_saved_tracks(market)
                data_list.append(data)

            elif sourcetype == 'playlist':
                playlist_data = self._get_playlist_dataframe(source_list=source['playlist'],
                                                             market=market)
                data_list.append(playlist_data)

            elif sourcetype == 'artist':
                artist_data = self._get_artist_dataframe(source_list=source['artist'],
                                                         market=market)
                data_list.append(artist_data)

        # concatinate the dataframes of all the source types and remove any duplicates
        data = pd.concat(data_list)
        data.drop_duplicates(inplace=True)

        return data


    def pick_tracks(self,
                    data_key,
                    time=25,
                    extra=5,
                    time_limit=None):
        """Using a specified dataset, this generates a subset of the dataframe of songs that fit the time constraints.

        Parameters
        ----------
        data_key : str
            Name of the dataset to use stored in the data object in Spomato
        time : int
            The length in minutes to make the playlist
        extra : type
            The amount of buffer time to add on to the end of the playlist.
        time_limit : type
            The maximum song length in minutes to include in the playlist.

        Returns
        -------
        pd.DataFrame
            A dataframe of song ids generated from the sources.

        """
        if not isinstance(data_key, str):
            raise TypeError('Argument data_key must be of type string')
        if not isinstance(time, (int, float)):
            raise TypeError('Argument time must be of type int or float')
        if not isinstance(extra, (int, float)):
            raise TypeError('Argument extra must be of type int or float')
        if time_limit is not None and not isinstance(time_limit, (int, float)):
            raise TypeError('Argument time_limit must be of type int or float')
        track_df = self.data[data_key]

        # the time in our dataframe is specified in seconds, we need to convert the times
        time *= 60
        extra *= 60

        # if time limit is not specified, default it to one third of the parameter time
        if time_limit is None:
            time_limit = time/3.0
        else:
            time_limit *= 60

        # filter out any records that are longer than the time limit
        track_df = track_df[track_df['time'] <= time_limit]

        # iterate adding songs to the selected track until the time is reached
        time_used = 0
        track_list = []
        done = False
        while not done:
            # filter down to tracks that fit in the remaining time
            track_df = track_df[track_df.time <= (time + extra - time_used)]

            # if the total time is greater than the specified time, mark the iteration done.
            if time_used > time:
                done = True
            # if the filtered song list is empty, there are no songs left, so mark iteration done
            elif track_df.empty:
                done = True
            # otherwise, take a random track from the dataframe, add to the track list, and remove it from being
            # selected again
            else:
                track = track_df.sample().iloc[0]
                track_df = track_df[track_df.song_id != track.song_id]
                track_list.append(track)
                time_used += track.time

        # concatinate all of the selected tracks into a dataframe.
        picked_track_df = pd.concat(track_list, axis=1).T

        return picked_track_df


    def _get_saved_tracks(self, market):
        """Access the spotify API to get the saved tracks for a user and returns a dataframe of song ids and times.

        Parameters
        ----------
        market : str
            A string representation of the Spotify market to filter on.

        Returns
        -------
        pd.DataFrame
            A dataframe of song ids generated from the sources.

        """
        # iterate over a user's saved tracks until all have been accessed and parsed
        end = False
        i = 0
        track_df_list = []
        while not end:
            data = self.spotipy_session.current_user_saved_tracks(limit=50, offset=i*50)['items']
            if len(data) > 0:
                track_df = self._parse_saved_tracks(data, market)
                track_df_list.append(track_df)
                i += 1
            else:
                end = True

        # concatinate the created dataframes and remove any duplicates
        track_df = pd.concat(track_df_list).reset_index(drop=True)
        track_df.drop_duplicates(inplace=True)

        return track_df


    def _get_artist_data(self, artist_id, market):
        """Access the spotify API to get an artist's tracks and returns a dataframe of song ids and times.

        Parameters
        ----------
        artist_id : type
            Description of parameter `artist_id`.
        market : str
            A string representation of the Spotify market to filter on.

        Returns
        -------
        pandas.DataFrame
            A dataframe of song ids and times generated from the sources.

        """
        # get all of the artist's albums ids and parse out the json for each
        artist_albums = self.spotipy_session.artist_albums(artist_id)
        album_ids = [x['id'] for x in artist_albums['items']]
        album_jsons = self.spotipy_session.albums(album_ids)['albums']

        # iterate over each album and parse out the songs
        songdf = []
        for album in album_jsons:
            if market in album['available_markets']:
                songs = self._parse_album(album, market)
                songdf.append(songs)

        # concatinate the results from each album into a single dataframe
        data = pd.concat(songdf)
        return data


    def get_playlists(self):
        """Access the spotify API to get the playlists for a user and returns a dataframe of names and ids.

        Returns
        -------
        pandas.DataFrame
            A dataframe consisting of the current user's playlist names and playlist ids.

        """
        # get the user's playlist and parse the playlist name and id
        pl_json = self.spotipy_session.current_user_playlists()
        series_index = ['playlist_name', 'playlist_id']
        playlist_list = [pd.Series([pl['name'], pl['id']], index=series_index) for pl in pl_json['items']]

        # concatinate the results into a pandas dataframe
        playlist_df = pd.concat(playlist_list, axis=1).T
        return playlist_df


    def make_playlist(self,
                      playlist_name,
                      song_df,
                      overwrite=False):
        """Create or overwrite a spotify playlist from the dataframe of songs.

        Parameters
        ----------
        playlist_name : str
            The name of the playlist you want to create/overwrite
        song_df : pandas.DataFrame
            Dataframe of songs to be in the playlist.
        overwrite : bool
            Boolean to determine whether to overwrite the playlist if it already exists.


        Returns
        -------
        None

        """
        if not isinstance(playlist_name, str):
            raise TypeError('Argument playlist_name must be of type string')
        if not isinstance(song_df, pd.DataFrame):
            raise TypeError('Argument song_df must be of type string')
        # get the user's playlists
        playlist_df = self.get_playlists()

        # if the playlist name already exists and is not set to be overwritten, raise an error
        if playlist_name in playlist_df.playlist_name.tolist() and not overwrite:
            raise ValueError('Playlist {p} already exists, set overwrite to True.'.format(p=playlist_name))

        # if the playlist already exists, replace the playlist with the new track list
        if playlist_name in playlist_df.playlist_name.tolist():
            playlist_id = playlist_df[playlist_df.playlist_name == playlist_name].iloc[0].playlist_id
            self.spotipy_session.user_playlist_replace_tracks(user=self.current_user_id,
                                                              playlist_id=playlist_id,
                                                              tracks=song_df.song_id.tolist()
                                                             )
        # if the playlist doesn't exist, create a new playlist with the track list
        else:
            self.spotipy_session.user_playlist_create(self.current_user_id,
                                                      playlist_name,
                                                      public=False)
            playlist_df = self.get_playlists()
            playlist_id = playlist_df[playlist_df.playlist_name == playlist_name].iloc[0].playlist_id
            self.spotipy_session.user_playlist_add_tracks(self.current_user_id,
                                                          playlist_id,
                                                          tracks=song_df.song_id.tolist()
                                                         )


    def pick_track_and_make_playlist(self,
                                     data_key,
                                     playlist_name,
                                     time=25,
                                     extra=5,
                                     time_limit=None,
                                     overwrite=False):
        """Picks the tracks from a created dataset and creates/overwrites a playlist with the data.

        Parameters
        ----------
        data_key : str
            Name of the dataset to use stored in the data object in Spomato
        playlist_name : str
            The name of the playlist you want to create/overwrite
        time : int
            The length in minutes to make the playlist
        extra : int
            The amount of buffer time to add on to the end of the playlist.
        time_limit : int
            The maximum song length in minutes to include in the playlist.
        overwrite : bool
            Boolean to determine whether to overwrite the playlist if it already exists.

        Returns
        -------
        None

        """
        if not isinstance(data_key, str):
            raise TypeError('Argument data_key must be of type string')
        if not isinstance(playlist_name, str):
            raise TypeError('Argument playlist_name must be of type string')
        if not isinstance(time, (int, float)):
            raise TypeError('Argument time must be of type int or float')
        if not isinstance(extra, (int, float)):
            raise TypeError('Argument extra must be of type int or float')
        if time_limit is not None and not isinstance(time_limit, (int, float)):
            raise TypeError('Argument time_limit must be of type int or float')
        # generate the list of songs for the playlist
        song_df = self.pick_tracks(data_key=data_key,
                                   time=time,
                                   extra=extra,
                                   time_limit=time_limit)

        # create the playlist with the song dataframe
        self.make_playlist(playlist_name=playlist_name,
                           song_df=song_df,
                           overwrite=overwrite)


    def artist_id_search(self,
                         artist,
                         limit=10,
                         offset=0):
        """Search the Spotify API for an artist and return the search results of matches and ids. This can be useful if
        you don't know an artist's id to generate a playlist.

        Parameters
        ----------
        artist : str
            Name of the artist to search. More complex searches can be run using the query guidelines in Spotipy.
        limit : int
            Number of records to return from search
        offset : int
            The number of records to skip in search result.

        Returns
        -------
        pandas.DataFrame
            A dataframe of artist names and ids from the search result.

        """
        if not isinstance(limit, int):
            raise TypeError('Argument limit must be of type int')
        if not isinstance(offset, int):
            raise TypeError('Argument offset must be of type int')
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
