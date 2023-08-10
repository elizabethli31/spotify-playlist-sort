import pandas as pd

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

def get_playlist_ids(sp):
    '''
    Returns list of each playlist id

    params
        - sp: spotify auth
    '''
    playlists = []
    for p in sp.current_user_playlists()['items']:
        playlists.append(p['id'])
    
    return playlists


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
    playlist_ids = get_playlist_tracks(playlist, sp)

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


def get_features(tracks, sp):
    '''
    Returns dataframe with each song in the list of tracks and their features

    params:
        - playlist: playlist ID
        - sp: spotify auth
    '''

    i = 0
    features = []
    for track in tracks:
        features.append(sp.audio_features(track))
    
    df = pd.DataFrame(features)[0].apply(pd.Series)
    df.insert(loc=0, column="name", value=tracks)
        
    return df

def get_playlist_data(playlists, sp):
    '''
    Returns a df containing data for each playlist

    params:
        - playlist: playlist ID
        - sp: spotify auth
    '''
    df = pd.DataFrame()

    for playlist in playlists['items']:
        
        # Build dataframe for songs currently in playlist
        tracks_in_playlist = get_playlist_tracks(playlist['id'], sp)
        df_playlist = get_features(tracks_in_playlist, sp)

        # Build dataframe for recommende songs
        #tracks_rec = get_recommended(playlist, sp)
        # df_rec = get_features(tracks_rec, sp)
        # df = pd.concat([df_in_playlist, df_rec])
        df_playlist['Playlist'] = playlist['id']
        df = pd.concat([df, df_playlist])
    
    return df

