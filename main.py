import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from songs import *


if __name__ == '__main__':

    # Authorization
    username = 'luigirdsoriano'
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    scope = 'user-library-read user-top-read playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)


    like_ids = []
    like_ids = sp.current_user_playlists()

    tracks = get_playlist_tracks("6XOle12412Xb9nI80M86XB", sp)


    print(get_playlist_data(get_playlist_ids(sp), sp))


