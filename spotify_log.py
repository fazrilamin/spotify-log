import os
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Read Spotify credentials from environment variables
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')

# Define the scope needed for reading recently played tracks
scope = "user-read-recently-played"

# Set up the Spotify OAuth manager
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    cache_path=".cache-spotify"  # Token is cached here after first authorization
)

sp = spotipy.Spotify(auth_manager=sp_oauth)

# Fetch the last 10 recently played tracks
results = sp.current_user_recently_played(limit=10)

# Append log entries to spotify_log.txt
with open("spotify_log.txt", "a") as log_file:
    log_file.write(f"Log on {datetime.datetime.now()}\n")
    for item in results['items']:
        track = item['track']
        played_at = item['played_at']
        track_name = track['name']
        artist_names = ", ".join([artist['name'] for artist in track['artists']])
        log_file.write(f"{played_at}: {track_name} by {artist_names}\n")
    log_file.write("\n")
