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
    
    
