import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import time
from spotipy.exceptions import SpotifyException

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.auth_manager = SpotifyOAuth(client_id = client_id,
                                         client_secret = client_secret,
                                         redirect_uri = redirect_uri,
                                         scope = scope)
        
        self.sp = spotipy.Spotify(auth_manager = self.auth_manager)

    def refresh_token(self):
        token_info = self.auth_manager.get_cached_token()
        if not token_info or self.auth_manager.is_token_expired(token_info):
            token_info = self.auth_manager.refresh_access_token(token_info['refresh_token'])
        return token_info['access_token']
    
    def search_and_queue_song(self, song_name):
        try:
            results = self.sp.search(q = song_name, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_uri = track['uri']
                self.sp.add_to_queue(track_uri)
                return track['name']
            return None
        except SpotifyException as e:
            print(f"Spotify API Error: {e}")
            return None
        except Exception as e:
            print("Unexpected Error occurred: {e}")
            return None
    
    def get_current_playback(self):
        try:
            playback = self.sp.current_playback()
            if playback and playback['is_playing']:
                return ['playback']['name']
            return "No song is currently playing"
        except SpotifyException as e:
            print(f"Spotify API Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error occured: {e}")
            return None
        
    def conmtrol_playback(self, action):
        try:
            if action == "play":
                self.sp.start_playback()
            elif action == "pause":
                self.sp.pause_playback()
            elif action == "next":
                self.sp.next_playback()
            elif action == "previous":
                self.sp.previous_playback()
        except SpotifyException as e:
            print(f"Spotfy API Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error occured: {e}")
            return None
        
    def create_playlist(self, playlist_name):
        try:
            user_id = self.sp.current_user()['id']
            playlist = self.sp.user_playlist_create(user_id, playlist)
            return playlist['id']
        except SpotifyException as e:
            print(f"Spotify API Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error occured: {e}")
            return None
        
    def add_track_to_playlist(self, playlist_id, track_uris):
        try:
            self.sp.playlist_add_items(playlist_id, track_uris)
        except SpotifyException as e:
            print(f"Spotify API Error: {e}")
        except Exception as e:
            print(f"Unexpected error occured: {e}")

    def load_playlist(self, playlist_id):
        try:
            results = self.sp.playlist_tracks(playlist_id)
            track_uris = [item["track"]["uri"] for item in results["items"]]
            for uri in track_uris:
                self.sp.add_to_queue(uri)
            return  [item["track"]["name"] for item in results["items"]]
        except SpotifyException as e:
            print(f"Spotify API Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error occured: {e}")
            return []
