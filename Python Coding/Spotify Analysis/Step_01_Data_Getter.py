""" Credits: Rommel Artola
& Spotify for providing the API services to extract data! (Thank you Spotify!)

This file is a quick and simple way to grab all of K Dot's songs along with a 
whole host of good and useful attributes of the songs. 

These attributes include Albums, dates, audio features, and rankings.

We end with a dataframe of 297 observations and 22 columns. (shape of 297,22)


This dataframe will be the foundational data for our analysis. Though,
we first need to clean it up in a seperate python script since it is currently
still very dirty with various duplicates.

Not exactly a very exciting file, so let's move along! The second file dives
more into how I'm actually cleaning up the data, so it has more visiblity into my
coding and logic (and thoughts alongside the steps I took).

Thought, if you pay close attention (if it hasn't been apparent yet), I'm just
analyzing the records of Kendrick Lamar, which is important for the future
files! So keep that in mind.. :)

"""


# Import Libraries
from spotipy import Spotify  
from spotipy.oauth2 import SpotifyOAuth  
import pandas as pd
from spotipy import SpotifyException
pd.options.display.max_columns=50

# Read in credentials (on .gitignore)
CLIENT_ID = open('client_id.txt').readline()
CLIENT_SECRET = open('client_secret.txt').readline()
REDIRECT_URI = 'https://sites.google.com/view/rommelartola/home/' # My Portfolio site.


sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
access_token = sp_oauth.get_access_token()  
sp = Spotify(auth_manager=sp_oauth)  

# Below try block will cycle through all of Kendrick's songs and append the 
# listed values to a dictionary, which will later be convereted to a pandas dataframe
## Another way of doing the same thing could've been a while loop with a += 50 at the 
## end of each step. For diagnostics purposes, I prefer try-except blocks many times more.

try:
    data_dict = {}
    for offset_num in range(0, 10_000+50, 50):
        for i in sp.search(q='artist:Kendrick Lamar', type='track', limit=50, offset=offset_num)['tracks']['items']:#.keys()

            data_dict.setdefault('ALBUM_ID', []).append(i['album']['id'])
            data_dict.setdefault('ALBUM_NAME', []).append(i['album']['name'])
            data_dict.setdefault('ALBUM_RELEASE_DATE', []).append(i['album']['release_date'])
            data_dict.setdefault('ALBUM_RELEASE_DATE_PRECISION', []).append(i['album']['release_date_precision'])
            data_dict.setdefault('TRACK_ID', []).append(i['id'])
            data_dict.setdefault('TRACK_NAME', []).append(i['name'])
            data_dict.setdefault('EXPLICIT_TRACK', []).append(i['explicit'])
            data_dict.setdefault('TRACK_POPULARITY', []).append(i['popularity'])
            data_dict.setdefault('TRACK_TYPE', []).append(i['type'])
            data_dict.setdefault('TRACK_DURATION_MS', []).append(i['duration_ms'])


            # Begin Specific Audio Features Per Song ID
            audio_feat_dict = sp.audio_features(i['id'])[0]
            data_dict.setdefault('TRACK_DANCEABILITY', []).append(audio_feat_dict['danceability'])
            data_dict.setdefault('TRACK_ENERGY', []).append(audio_feat_dict['energy'])
            data_dict.setdefault('TRACK_KEY', []).append(audio_feat_dict['key'])
            data_dict.setdefault('TRACK_LOUDNESS', []).append(audio_feat_dict['loudness'])
            data_dict.setdefault('TRACK_MODE', []).append(audio_feat_dict['mode'])
            data_dict.setdefault('TRACK_SPEACHINESS', []).append(audio_feat_dict['speechiness'])
            data_dict.setdefault('TRACK_ACOUSTICNESS', []).append(audio_feat_dict['acousticness'])
            data_dict.setdefault('TRACK_INSTRUMENTALNESS', []).append(audio_feat_dict['instrumentalness'])
            data_dict.setdefault('TRACK_LIVENESS', []).append(audio_feat_dict['liveness'])
            data_dict.setdefault('TRACK_VALENCE', []).append(audio_feat_dict['valence'])
            data_dict.setdefault('TRACK_TEMPO', []).append(audio_feat_dict['tempo'])
            data_dict.setdefault('TRACK_TIME_SIGNATURE', []).append(audio_feat_dict['time_signature'])

except SpotifyException as e:
    print(f'Offset Limit Reached: {e}')

df = pd.DataFrame(data_dict)