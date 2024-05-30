import requests
import pymongo
from pymongo import MongoClient

def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    return auth_response.json().get('access_token')

def get_playlist_data(token, playlist_id):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {
        'limit': 100,
        'offset': 0
    }
    all_tracks = []
    while True:
        response = requests.get(playlist_url, headers=headers, params=params)
        data = response.json()
        all_tracks.extend(data['items'])
        if data['next']:
            params['offset'] += params['limit']
        else:
            break
    return all_tracks

def extract_data(tracks):
    tracks_data = []
    artist_ids = set()
    for item in tracks:
        track = item['track']
        if track:  # Check if track data is present
            track_info = {
                'track_name': track['name'],
                'track_id': track['id'],
                'artist_name': track['artists'][0]['name'],
                'artist_id': track['artists'][0]['id'],
                'album_name': track['album']['name'],
                'album_id': track['album']['id']
            }
            tracks_data.append(track_info)
            artist_ids.add(track['artists'][0]['id'])
    return tracks_data, artist_ids

def get_artist_data(token, artist_ids):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    artist_data = []
    for artist_id in artist_ids:
        response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=headers)
        artist_data.append(response.json())
    return artist_data

def connect_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['spotify']
    return db

def insert_data(collection, data):
    collection.insert_many(data)

if __name__ == '__main__':
    client_id = '81fb295a64774dc08eeac1267aec9f2b'
    client_secret = 'dafbe1738a084c038670a46bf0806ddc'
    playlist_id = 'your_playlist_id'
    
    token = get_spotify_token(client_id, client_secret)
    playlist_tracks = get_playlist_data(token, playlist_id)
    extracted_data, artist_ids = extract_data(playlist_tracks)
    
    db = connect_mongo()
    
    # Insert tracks data
    tracks_collection = db['playlist_tracks']
    insert_data(tracks_collection, extracted_data)
    
    # Fetch and insert artist data
    artist_data = get_artist_data(token, artist_ids)
    artists_collection = db['artists']
    insert_data(artists_collection, artist_data)
