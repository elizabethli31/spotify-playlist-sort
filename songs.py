import pandas as pd

def get_user_top_tracks(sp):
    '''
    Returns list of IDs of the user's top songs

    params: spotify auth
    '''
    ids = []

    # User Top Tracks
    results = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
    tracks = results['items']

    i = 0
    for i in range(len(tracks)):
        ids.append(tracks[i]['id'])


    # User Top Artists
    results = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
    artists = []
    for result in results['items']:
        artists.append(result['id'])
    
    i = 0
    for i in range(len(artists)):
        tracks = sp.artist_top_tracks(artists[i], country='US')
        for track in tracks['tracks']:
            ids.append(track['id'])

    return ids

def get_user_saved_tracks(sp, n):
    '''
    Gets n*50 of the users most recently saved tracks
    
    params
        - sp
        - n: number of iterations
    '''
    ids = []

    results = sp.current_user_saved_tracks(limit=50, offset=0)
    tracks = results['items']

    while results['next'] and n>0:
        results = sp.next(results)
        tracks.extend(results['items'])
        n -= 1

    i = 0
    for i in range(len(tracks)):
        ids.append(tracks[i]['track']['id'])

    return ids

def get_playlist_tracks(playlist, sp):
    '''
    Returns list of ids of all songs from a playlist

    params
        - playlist: playlist ID
        - sp: spotify auth
    '''
    ids = []

    tracks = sp.playlist_tracks(playlist, limit=100, offset=0)

    while tracks:
        for song in tracks['items']:
            ids.append(song['track']['id'])
    
        if tracks['next']:
            tracks = sp.next(tracks)
        else:
            break
    
    return ids

def get_recommended(playlist, sp):
    '''
    Returns list of ids of recommended tracks based on a playlist

    params:
        - playlist: playlist ID
        - sp: spotify auth
    '''
    playlist_ids = get_playlist_tracks([], playlist, sp)

    ids = []

    tracks = sp.recommendations(seed_tracks=playlist_ids, limit=100)

    while tracks:
        for song in tracks['items']:
            ids.append(song['track']['id'])
    
        if tracks['next']:
            tracks = sp.next(tracks)
        else:
            break
    
    return ids


def get_features(features, like, dislike, sp):

    i = 0
    for i in range(len(like)):
        audios = sp.audio_features(like[i])

        for audio in audios:
            features.append(audio)
            features[-1]['target'] = 1

    i = 0
    for i in range(len(dislike)):
        audios = sp.audio_features(dislike[i])

        for audio in audios:
            features.append(audio)
            features[-1]['target'] = 0

    return pd.DataFrame(features)

