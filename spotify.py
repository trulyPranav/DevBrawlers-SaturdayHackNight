import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import random

CLIENT_ID = ''
CLIENT_SECRET = ''
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
def profile_tab():
    st.title("Your Spotify Profile")
    
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
            st.write(user_data)
            st.write("User Profile:")
            st.write(f"Display Name: {user_data['display_name']}")
            st.write(f"Country: {user_data['country']}")
        else:
            st.write("Failed to fetch user profile data.")
    else:
        auth_url = auth_manager.get_authorize_url()
        st.write(f"Please go to the following URL to authorize: [Login with Spotify]({auth_url})")

def main():
    st.title("Spotify Music Recommendation")
    st.write("Log in to Spotify to get music recommendations based on your top artists.")

    st.sidebar.title("Navigation")
    tabs = ["RcordiX","Profile"]
    choice = st.sidebar.radio("Go to:", tabs)

    auth_manager = get_spotify_auth()
    if choice == "RcordiX":
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
    elif choice == "Profile":
        profile_tab()
    else:
        auth_url = auth_manager.get_authorize_url()
        if st.button("Login"):
            st.query_params.auth = True
            st.write(f"Please go to the following URL to authorize: [Login with Spotify]({auth_url})")

if __name__ == "__main__":
    main()