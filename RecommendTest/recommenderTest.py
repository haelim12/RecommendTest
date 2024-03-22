import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
import pickle

from data import Session
from model.track import Track

session = Session()


# 특징 데이터 가져오기
def get_feature_data(session):
    # 실제 데이터베이스 스키마 및 구조에 따라 수정이 필요할 수 있습니다.
    # 예시로 사용자 ID, 트랙 ID, acousticness, danceability, energy 열을 가진 데이터프레임을 반환한다고 가정
    result = session.query(Track).all()
    return result


# 전체 트랙 데이터 가져오기
def get_all_track_features(session):
    result = session.query(Track).all()
    return result


saved_model_fname = "model/finalized_model.sav"

def model_train():

    # 특징 데이터 가져오기
    features_df = pd.DataFrame(get_feature_data(session))

    # 좋아요 데이터 가져오기
    likes_df = pd.DataFrame(get_all_track_features(session))

    # 필요한 특징 열만 추출
    features_subset = features_df[['spotify_id', 'feature_acousticness', 'feature_danceability', 'feature_energy']]

    # 좋아요 데이터와 특징 데이터를 병합
    merged_df = pd.merge(likes_df, features_subset, on='spotify_id')

    # 좋아요 데이터와 특징 데이터를 포함한 데이터프레임을 사용하여 모델 학습
    like_matrix = coo_matrix(
        (merged_df["rating"].astype(np.float32),
         (merged_df["spotify_id"].astype("category").cat.codes.copy(),
          merged_df["user_id"].astype("category").cat.codes.copy(),
          )
         )
    )

    als_model = AlternatingLeastSquares(
        factors=50,  # 특징 수에 맞게 조절
        regularization=0.01,
        iterations=50
    )

    als_model.fit(like_matrix.T)

    # 학습된 모델 저장
    pickle.dump(als_model, open(saved_model_fname, "wb"))
    return als_model


if __name__ == "__main__":
    model = model_train()
