import os
# OpenBLAS의 내부 스레드 풀 비활성화
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix  # Import csr_matrix
from implicit.als import AlternatingLeastSquares
import pickle

from data import Session
from model.track import Track

session = Session()

# 트랙 데이터 가져오기
def get_track_by_spotify_id(spotify_id: str, session):
    result = session.query(Track).filter(Track.spotify_id == spotify_id).one_or_none()
    return result

track = get_track_by_spotify_id('347AQK5Lyhn6RvB8tBGYxt', session)
print(track.title)

# 트랙 정보를 담은 DataFrame 생성
track_data = {
    'spotify_id': [track.spotify_id],
    'track_id': [track.track_id],
    'acousticness': [track.feature_acousticness],
    'danceability': [track.feature_danceability],
    'energy': [track.feature_energy]
}

def get_recommendations(liked_tracks, session, num_recommendations=5):
    # 사용자가 좋아요한 노래들의 특성을 추출
    liked_track_features = []
    for track_id in liked_tracks:
        track = get_track_by_spotify_id(track_id, session)
        if track:
            liked_track_features.append([track.feature_acousticness, track.feature_danceability, track.feature_energy])

    # 특성을 numpy 배열로 변환
    liked_track_features = np.array(liked_track_features)

    # ALS 모델 훈련을 위해 희소 행렬로 변환
    sparse_matrix = csr_matrix(liked_track_features.T)  # Convert to CSR matrix

    # ALS 모델 초기화 및 훈련
    als_model = AlternatingLeastSquares(factors=50)
    als_model.fit(sparse_matrix)

    # 추천을 위해 유사한 아이템 찾기
    similar_items = als_model.similar_items(itemid=0, N=num_recommendations)

    # 추천 결과를 담을 리스트
    recommendations = []

    # 추천된 노래들의 Spotify ID 가져오기, 제외한 후 리스트에 추가
    for item in similar_items:
        # item[0]를 정수로 변환하여 사용
        track_id = liked_tracks[int(item[0])]
        if track_id not in liked_tracks:
            recommendations.append(track_id)

    return recommendations

# 좋아요한 노래들의 Spotify ID 리스트
liked_tracks = ['347AQK5Lyhn6RvB8tBGYxt', '2y4ZR0BUAVePljHSsZyIgj', '2yyO7EKRr7c3txi4xCXUFk']

# 추천 받기
recommended_tracks = get_recommendations(liked_tracks, session)

print("추천된 노래들:")
for track_id in recommended_tracks:
    track = get_track_by_spotify_id(track_id, session)
    print(f"Track ID: {track_id}, Title: {track.title}, acousticness: {track.feature_acousticness}, danceability: {track.feature_danceability}, energy: {track.feature_energy}")
    print("=====================================")  # 구분선
