import os

import spotipy
from pydantic_core.core_schema import none_schema
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

def test_spotify_connection():
    """
    Test connection to Spotify API using Spotipy
    :return: Spotipy object with for the respective track
    """
    try:
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Spotify client ID or secret not found in environment variables.")

        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

        test_track = "Beg"
        test_artist = ("Saliva")

        print(f"\nSearching for: {test_track} by {test_artist}")
        results = sp.search(q=f"track:{test_track} artist:{test_artist}",
                        type='track', limit=1)

        if results["tracks"]["items"]:
            track= results["tracks"]["items"][0]
            track_id = track["id"]

            print("Found track: {0} by {1}".format(track["name"], track["artists"][0]["name"]))
            print("Spotify ID: {0}".format(track_id))


            features = sp.audio_features([track_id])[0]
            print(f"\nAudio features retrieved successfully!")
            print(f"   Danceability: {features['danceability']}")
            print(f"   Energy: {features['energy']}")
            print(f"   Valence: {features['valence']}")

            return sp
        else:
            print("Track not found try again")
            return None
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    sp = test_spotify_connection()

    if sp:
        print("Spotify API works lfg!!")

    else:
        print("Try again...")


