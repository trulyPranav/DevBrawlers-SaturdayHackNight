import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import random

home,user,library = st.tabs(["Home","Profile","Library"])

# This ID and SECRET is for development purposes only!
# For production, there lies a deployment option, which we have not activated
# So for using this app, I'll have to authorize
# Kindly contact if needed

CLIENT_ID = '70e397a870904fd680bdc835d261eb20'
CLIENT_SECRET = '3744f451901042928eb87666bbecbcf8'
REDIRECT_URI = 'http://localhost:8501/'

# Set the scope to access user's top artists and tracks
SCOPE = 'user-top-read,user-read-private'

def get_spotify_auth():
    return SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

def get_top_artists(sp):
    top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
    return top_artists['items']

# Function to fetch user's playlists and their tracks
def get_user_playlists(sp):
    playlists = sp.current_user_playlists()
    return playlists['items']

# Function to fetch tracks of a specific playlist
def get_playlist_tracks(sp, playlist_id):
    tracks = sp.playlist_tracks(playlist_id)
    return tracks['items']

def recommend_music(sp):
    top_artists = get_top_artists(sp)
    
    related_artists = []
    for artist in top_artists:
        related_artists.extend(sp.artist_related_artists(artist['id'])['artists'])
    
    related_artist_names = [artist['name'] for artist in related_artists]
    
    unique_related_artists = []
    for artist in related_artists:
        if artist['name'] not in [top_artist['name'] for top_artist in top_artists]:
            unique_related_artists.append(artist)
    
    random.shuffle(unique_related_artists)
    return unique_related_artists[:5]

# Streamlit UI

with home:
    st.title('Welcome to RcordiX')
    rec1, rec2, rec3, rec4, rec5 = st.columns((1, 1, 1, 1, 1))
    rec_list = [rec1, rec2, rec3, rec4, rec5]

    auth_manager = get_spotify_auth()
    token_info = auth_manager.get_cached_token()
    if token_info:
        sp = Spotify(auth=token_info['access_token'])
        if st.button("Get Recommendations"):
            recommended_artists = recommend_music(sp)
            if recommended_artists:
                for i, artist in enumerate(recommended_artists):
                    with rec_list[i]:
                        st.markdown(f"### ***{artist['name']}***")
                        st.image(f"{artist['images'][0]['url']}", width=100)
                        tracks = sp.artist_top_tracks(artist['id'])
                        st.write(f"Tracks for {artist['name']}:")
                        for track in tracks['tracks']:
                            st.write(f"- {track['name']}")
                            st.write("Song Preview:")
                            audio_url = track['preview_url']
                            if audio_url:
                                st.audio(audio_url, format='audio/mp3', start_time=0)
                            else:
                                st.write("No preview available for this track.")
    else:
        auth_url = auth_manager.get_authorize_url()
        if st.button("Login", key="login_button1"):
            st.query_params.auth = True
            st.write(f"Please go to the following URL to authorize: [Login with Spotify]({auth_url})")

with user:
    st.title("Your Spotify Profile")
    with st.container(height=300):
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
            
            # Get user profile data
            user_data = sp.current_user()
            
            if user_data:
                if user_data['images']:
                    st.image(user_data['images'][0]['url'], width=100)
                    st.write(f"### Name: {user_data['display_name']}")
                    st.write(f"### Country: {user_data['country']}")
                else:
                    st.write(f"### Name: {user_data['display_name']}")
                    st.write(f"### Country: {user_data['country']}")
            else:
                st.write("Failed to fetch user profile data.")
        else:
            auth_url = auth_manager.get_authorize_url()
            st.write(f"Please go to the following URL to authorize: [Login with Spotify]({auth_url})")

with library:
    st.title("Your Spotify Library")

    # Authenticate with Spotify
    auth_manager = get_spotify_auth()
    token_info = auth_manager.get_cached_token()

    if token_info:
        sp = Spotify(auth=token_info['access_token'])

        # Get user's playlists
        playlists = get_user_playlists(sp)

        if playlists:
            # Create a dropdown menu to select playlists
            selected_playlist_name = st.selectbox("Select Playlist", [playlist['name'] for playlist in playlists])

            # Find the selected playlist
            selected_playlist = next((playlist for playlist in playlists if playlist['name'] == selected_playlist_name), None)

            if selected_playlist:
                # Get tracks of the selected playlist
                playlist_tracks = get_playlist_tracks(sp, selected_playlist['id'])

                if playlist_tracks:
                    st.write(f"### Playlist: {selected_playlist_name}")

                    for track in playlist_tracks:
                        track_name = track['track']['name']
                        track_artist = track['track']['artists'][0]['name']
                        track_preview_url = track['track']['preview_url']

                        st.write(f"- {track_name} by {track_artist}")

                        if track_preview_url:
                            st.audio(track_preview_url, format='audio/mp3', start_time=0)
                        else:
                            st.write("No preview available for this track.")
                else:
                    st.write("No tracks available in this playlist.")
            else:
                st.write("Please select a playlist.")
        else:
            st.write("No playlists found.")

    else:
        auth_url = auth_manager.get_authorize_url()
        if st.button("Login", key="login_button2"):
            st.query_params.auth = True
            st.write(f"Please go to the following URL to authorize: [Login with Spotify]({auth_url})")