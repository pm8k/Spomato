# Spomato

Welcome!

This project is intended to be a way to generate playlists through the Spotify API. The main purpose was to create a
Tomato Timer length playlist in Spotify (Spotify + Tomato = Spomato).

## Installation
You can install via pypi:
```
pip install spomato
```

You can pip install it straight from git:
```
pip install git+git://github.com/pm8k/spomato.git
```


## Spotify Access Token

You need to have a Spotify Access token in order to access the Spotify API. The API scopes used by this library are
playlist-read-private, playlist-modify-private, and user-library-read.

You can find the [Spotify Authorization flow here](https://developer.spotify.com/documentation/general/guides/authorization-guide/)
and you can find the [Spotipy implementation here](https://spotipy.readthedocs.io/en/2.12.0/#authorization-code-flow).

## Using Spomato

### Create a Spomato object with a Spotify Access Token:

Create a Spomato object providing your token.
```
sp = spomato.Spomato(access_token='your-token')
```

### Creating a Dataset

The first step is to create one or more datasets to use as a source for your playlist.

#### Creating a Dataset from Your Saved Tracks

You can use the user's saved tracks as your dataset. This is the default, or you can specify it as below:

```
sp.get_api_data(data_key='your_dataset_name',
                source={'savedtracks':None})
```

#### Creating a Dataset from Your Playlist(s)

You can use the user's playlist(s) as your dataset.

```
sp.get_api_data(data_key='your_dataset_name',
                source={'playlist':['playlistid1','playlistid2']})
```

#### Creating a Dataset from an Artist

You can use any number of artists to create your dataset.

```
sp.get_api_data(data_key='your_dataset_name',
                source={'artist':['artistid1','artistid2']})
```

#### Creating a Dataset from Multiple Sources

You can use any of the above sources to create a dataset.

```
sp.get_api_data(data_key='your_dataset_name',
                source={'artist':['artistid1','artistid2'], 'playlist':['playlistid4', 'savedtracks':None]})
```

#### Additional Arguments

There are a few more arguments you can pass to generate a dataset:
 - file_path: If you want to save the dataset to file, pass in a path to a file to save a csv of your dataset
 - reset: A boolean to determine if you want to overwrite a dataset you've previously created
 - market: The Spotify market to filter the songs that can be added to a playlist

#### Read the Dataset from File

If you saved the file, you can also use that to load it back into a dataset:


```
sp.get_file_data(data_key='default',
                 file_path='/my/path/data.csv',
                 overwrite=False)
```

### Searching Data
 You can find an artist or playlist id you're looking for with a couple builtin functions.
```
 playlist_df = sp.get_playlists()
```
The `get_playlists()` function returns all of your playlists by name and id.
```
artist_search_df = sp.artist_id_search(artist='Foo Fighters')
```
The `artist_id_search` function will search a given string for artists of that name, returning DataFrame of artists and their ids.

You can alternatively go through Spotify and find the corresponding id in the web url when you click on the corresponding playlist or artist.

### Creating a Playlist

#### Get the Song List to Create a playlist

You can use our built in function to select tracks from a dataset to make your playlist.

```
my_song_df = sp.pick_tracks(data_key='my_dataset', time=25, extra=5)
```
This example will create a playlist between 25 and 30 minutes. It selects tracks until the total time is greater than
or equal to the `time` argument in minutes but not that it exceeds `time + extra` (also in minutes). You can
also specify a maximum song length with the `time_limit` argument (the default is one-third of `time`).

You can also generate you own dataframe using your own logic. You can access a dataset by:
```
dataset_df = sp['data']['my_dataset']
```

### Create the Playlist

Once you have the dataframe of your songs generated, you can create the playlist.
```
sp.make_playlist(playlist_name='New_Playlist_Name', song_df=my_song_df)
```
