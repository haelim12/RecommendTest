import requests


def get_spotify_access_token(client_id, client_secret):
    # Spotify API 엑세스 토큰을 가져오기 위한 함수
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    auth = (client_id, client_secret)

    response = requests.post(url, headers=headers, data=data, auth=auth)
    access_token = response.json().get('access_token')

    return access_token


def get_audio_features(track_id, access_token):
    # Spotify API를 통해 트랙의 오디오 특성값을 가져오기
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)
    audio_features_data = response.json()

    return audio_features_data


def get_spotify_recommendations(access_token, seed_track_id, target_acousticness, target_danceability, target_energy,
                                target_valence, limit=5):
    # Spotify API를 통해 유사한 음악을 검색하기
    url = 'https://api.spotify.com/v1/recommendations'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

    params = {
        'seed_tracks': seed_track_id,
        'target_acousticness': target_acousticness,
        'target_danceability': target_danceability,
        'target_energy': target_energy,
        'target_valence': target_valence,
        'limit': limit,
    }

    response = requests.get(url, headers=headers, params=params)
    recommendations_data = response.json()

    return recommendations_data


# Spotify API 계정 정보
client_id = '8fc753e32c4848c48bdd29b24c92ee53'
client_secret = '414b7bfaf02b47c28d08a8223d801bff'

# 사용자가 선택한 노래의 Spotify 트랙 ID (실제 값으로 변경)
seed_track_id = '2takcwOaAZWiXQijPHIx7B'

# 사용자가 선택한 노래의 특성값 가져오기
access_token = get_spotify_access_token(client_id, client_secret)
seed_track_features = get_audio_features(seed_track_id, access_token)

# 추천을 받을 노래의 특성값 설정
target_acousticness = seed_track_features['acousticness']
target_danceability = seed_track_features['danceability']
target_energy = seed_track_features['energy']
target_valence = seed_track_features['valence']

# 추천 받은 노래 가져오기
recommendations_data = get_spotify_recommendations(access_token, seed_track_id, target_acousticness,
                                                   target_danceability, target_energy, target_valence)

# 추천된 노래 출력
recommended_tracks = recommendations_data.get('tracks', [])
for track in recommended_tracks:
    track_id = track['id']
    track_name = track['name']
    track_artists = ', '.join([artist['name'] for artist in track['artists']])
    print(f"Track: {track_name}, Artists: {track_artists}, Track ID: {track_id}")

    # 각 추천된 트랙의 상세 정보를 가져와서 출력
    track_details = get_audio_features(track_id, access_token)
    print(f"Preview URL: {track['preview_url']}")
    print(f"Acousticness: {track_details['acousticness']}")
    print(f"Danceability: {track_details['danceability']}")
    print(f"Valence: {track_details['valence']}")
    print("\n")
