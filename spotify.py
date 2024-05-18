import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import random

CLIENT_ID = 'ea06b89dd4b6494682b3b51a990e22fe'
CLIENT_SECRET = '503b9737cf56429b96372406ce5eaf89'
REDIRECT_URI = 'http://localhost:8501/'

# Set the scope to access user's top artists and tracks
SCOPE = 'user-top-read'

def get_spotify_auth():
    return SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

def get_top_artists(sp):
    """Fetch the user's top artists from Spotify."""
    top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
    return top_artists['items']

def recommend_music(sp):
    """Generate music recommendations based on the user's top artists."""
    top_artists = get_top_artists(sp)
    
    # Get related artists for each top artist
    related_artists = []
    for artist in top_artists:
        related_artists.extend(sp.artist_related_artists(artist['id'])['artists'])
    
    # Extract names of related artists
    related_artist_names = [artist['name'] for artist in related_artists]
    
    # Filter out duplicates and top artists
    unique_related_artists = []
    for artist in related_artists:
        if artist['name'] not in [top_artist['name'] for top_artist in top_artists]:
            unique_related_artists.append(artist)
    
    # Shuffle and return random recommendations
    random.shuffle(unique_related_artists)
    return unique_related_artists[:5]

# Streamlit UI
st.title("Spotify Music Recommendation")
st.write("Log in to Spotify to get music recommendations based on your top artists.")

auth_manager = get_spotify_auth()

# Handle Spotify OAuth callback
query_params = st.query_params
if 'code' in query_params:
    code = query_params['code']
    token_info = auth_manager.get_access_token(code)
    st.query_params.clear()  # Clear the query params

token_info = auth_manager.get_cached_token()

if token_info:
    sp = Spotify(auth=token_info['access_token'])
    if st.button("Get Recommendations"):
        recommended_artists = recommend_music(sp)
        if recommended_artists:
            st.markdown("## Recommended artists:")
            for artist in recommended_artists:
                st.markdown(f"### ***{artist['name']}***")
                st.image(f"{artist['images'][0]['url']}", width=200)
                st.write("Tracks:")
                tracks = sp.artist_top_tracks(artist['id'])
                for track in tracks['tracks']:
                    st.write(f"- {track['name']}")
        else:
            st.write("No recommended artists found.")
else:
    auth_url = auth_manager.get_authorize_url()
    if st.button("Login"):
        st.query_params.auth = True
        st.write(f"Please go to the following URL to authorize: [Login with Spotify]({auth_url})")