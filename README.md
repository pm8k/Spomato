# Spomato

Welcome!

This project is intended to be a way to generate playlists through the Spotify API. The main purpose was to create a number of Tomato Timer length playlists through Spotify (hence the name Spomato, yeah, its silly). 

## Installation

You can pip install it straight from git:
```
pip install git+git://github.com/pm8k/spomato.git
```

You will also need to install the driver for chrome:
```
brew install chromedriver
```

## Set up Spotipy

### Create Spotify Application

You will need to create an application for your use as detailed in the [Spotipy](https://spotipy.readthedocs.io/en/latest/#authorized-requests) documentation.

### Set Environment Variables

The token generation uses [Spotipy's](http://spotipy.readthedocs.io/en/latest/#authorization-code-flow) Authorization Code Flow from the Spotify API. Make sure to correctly set up Spotipy through their tutorial, and set the following environment variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secre'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Set Up Spomato

### Set Environment Variables

As Spomato logs into your Spotify account information to log in, you will need to set these as environment variables.
```
export SPOMATO_USERNAME='your@email.com'
export SPOMATO_PASSWORD='password'
```
This works for a Spotify account and a Facebook account. You need to make sure you declare which log in method you are using when you create your token.

## Using Spomato

### Create a Token and Connection

Creating a connection to Spotify is easy:
```
token,token_info = get_token()
sp = spotipy.Spotify(auth=token)
```

### Fetching Data


The first step you will need is a data source.

```
df = get_data(sp=sp, profile_name='liked_songs', reset=False)
 ```

You can fetch the corresponding data and return it to a pandas DataFrame. The default source is ```savedtracks```, which pulls from songs you've saved through Spotify. You can also specify an `artist` (or multiple artists) by providing a list of artist_ids through the `sourcelist` argument or a `playlist` (or multiple playlists) by providing a list of playlist names through the `sourcelist` argument.

You can also specify a `profile_name` for your playlist. If that profile has not already been created, it will create a saved data set for you (so you do not need to fetch it from spotify every time). Every future call to that profile_name will locally read the data. If you wish to update your list (to include new saved songs or new albums for an artist) you can set `reset=True` in your `get_data` function call.


 ### Searching Data
 You can find an artist or playlist id you're looking for with a couple builtin functions.
```
 playlist_df = get_playlists(sp)
```
The `get_playlists()` function returns all of your playlists by name and id.
```
artist_search_df = artist_id_search(sp,artist='Foo Fighters')
```
The `artist_id_search` function will search a given string for artists of that name, returning DataFrame of artists and their ids.

You can alternatively go through Spotify and find the corresponding id in the web url when you click on the corresponding playlist or artist.

### Creating a Playlist
Here is a sample piece of code to create a playlist:
```
target_playlist = 'Spomato Timer'
user_id = sp.current_user()['id']
songdf, df = pick_songs(df, time=55, extra=5)
make_playlist(sp, target_playlist, songdf, user_id)
```

This does 3 things: it grabs the id of the current_user, it picks songs from the target list of songs you generated into a new DataFrame, then it will go and make that playlist with those songs.

The `time` argument specifies, in minutes, how long you want the playlist to be. The pick songs function will then go and grab songs to fill your playlist until the time is filled, ensuring that the playlist will not be longer than `time + extra`. You can also specify a maximum song length with the `time_limit` argument (the default is one-third of the time).
