import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from songs import *
from model import *


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

    
    playlists = []
    playlists = sp.current_user_playlists()

    print("getting playlist data")
    df = get_playlist_data(playlists, sp)

    print('training')
    train(df, sp)

    # calculate accuracy
    predicted = pd.read_csv('elizabethsongs.csv')
    correct = 0
    total = 0
    for index, row in predicted.iterrows():
        if row['Playlist'] == row['Predicted Playlist']:
            correct += 1
        total += 1
    print(correct/total)





