import requests
import json


def get_audio_features(track_id, access_token):
    # Spotify API를 통해 트랙의 오디오 특성값을 가져오기
    endpoint = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(endpoint, headers=headers)
    audio_features_data = response.json()

    return audio_features_data


def recommend_music(audio_features):
    # Spotify API 엑세스 토큰을 설정하세요. 필요하다면 Spotify Developer Dashboard에서 획득 가능합니다.
    access_token = "BQDkGf3kIG_davwdotojpEbe9gZ0CaqunA43-CEYmZmHwR2aoVMSBJncQZL47GRr-lQluYn5WVfEE_DSNwMde4TlLFINTVnHi8c_rKVmDZjkEZKdV2k"

    # 추천 기준으로 사용할 음악 특성값 가져오기
    target_acousticness = audio_features[0]["acousticness"]
    target_danceability = audio_features[0]["danceability"]
    target_valence = audio_features[0]["valence"]

    # Spotify API를 통해 유사한 음악을 검색하기
    endpoint = "https://api.spotify.com/v1/recommendations"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    params = {
        "seed_tracks": audio_features[0]["id"],
        "target_acousticness": target_acousticness,
        "target_danceability": target_danceability,
        "target_valence": target_valence,
        "limit": 5  # 추천 받을 음악의 개수를 설정하세요.
    }

    response = requests.get(endpoint, headers=headers, params=params)
    recommendation_data = response.json()

    # 출력하여 데이터 확인
    # print("Raw Recommendation Data:")
    # print(json.dumps(recommendation_data, indent=2))  # 들여쓰기를 사용하여 보기 쉽게 출력

    # 추천된 음악 리스트 출력
    if "tracks" in recommendation_data:
        recommended_tracks = recommendation_data["tracks"]
        print("Recommended Tracks:")
        for track in recommended_tracks:
            # 트랙의 오디오 특성값 가져오기
            track_audio_features = get_audio_features(track["id"], access_token)

            print(f"Track: {track['name']}, Artist: {track['artists'][0]['name']}")
            print(f"Preview URL: {track['preview_url']}")
            print(f"Acousticness: {track_audio_features['acousticness']}")
            print(f"Danceability: {track_audio_features['danceability']}")
            print(f"Valence: {track_audio_features['valence']}")
            print("-----")
    else:
        print("Error in getting recommendations.")


# 사용 예시
audio_features_data = {
    "audio_features": [
        {
            "acousticness": 0.00242,
            "danceability": 0.585,
            "duration_ms": 237040,
            "energy": 0.842,
            "id": "2takcwOaAZWiXQijPHIx7B",
            "instrumentalness": 0.00686,
            "key": 9,
            "liveness": 0.0866,
            "loudness": -5.883,
            "mode": 0,
            "speechiness": 0.0556,
            "tempo": 118.211,
            "time_signature": 4,
            "track_href": "https://api.spotify.com/v1/tracks/2takcwOaAZWiXQijPHIx7B",
            "type": "audio_features",
            "uri": "spotify:track:2takcwOaAZWiXQijPHIx7B",
            "valence": 0.428
        }
    ]
}

recommend_music(audio_features_data["audio_features"])
