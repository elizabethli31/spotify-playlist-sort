import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.metrics import accuracy_score

def train(df, sp):
    '''
    Trains K-nearest neighbors model given a dataframe to predict playlist it would be in 

    params:
        - df: datframe of
    '''
    X = df[['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key'
            , 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']]
    y = df['Playlist']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size = .75)

    # Scale features
    # scale= StandardScaler()    
    # X_train = scale.fit_transform(X_train)    
    # X_test = scale.transform(X_test)  
    X_train = normalize(X_train)
    X_test = normalize(X_test)

    # Train model
    knn = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2 )  
    knn.fit(X_train, y_train) 

    y_pred = knn.predict(X_test)
    print(accuracy_score(y_test, y_pred))

    # Assuming 'df' is your DataFrame with 'name' and 'Playlist' columns
    df['Predicted Playlist'] = knn.predict(X)

    print("get here")

    # Retrieve track and playlist names using Spotify API
    def get_track_name(track_id):
        return sp.track(track_id)['name']

    def get_playlist_name(playlist_id):
        return sp.playlist(playlist_id)['name']

    df['name'] = df['name'].apply(get_track_name)
    # df['Playlist'] = df['Playlist'].apply(get_playlist_name)
    # df['Predicted Playlist'] = df['Predicted Playlist'].apply(get_playlist_name)

    path = os.path.join(os.getcwd(), 'elizabethsongs.csv')
    df[['name', 'Playlist', 'Predicted Playlist']].to_csv(path)




    