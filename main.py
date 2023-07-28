import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from songs import *

if __name__ == '__main__':

    # Authorization
    username = 'elizabethli313'
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    scope = 'user-library-read user-top-read playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)


    like_ids = []
    like_ids = get_user_top_tracks(like_ids, sp)

    print(like_ids[0])


