import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data import Session
from model.track import Track

session = Session()

# 특징 데이터 가져오기
def get_feature_data(session):
    result = session.query(Track.title, Track.spotify_id, Track.feature_acousticness, Track.feature_danceability, Track.feature_energy).all()
    return result

# 전체 트랙 데이터 가져오기
def get_all_track_features(session):
    result = session.query(Track).all()
    return result

def get_title_from_spotify_id(spotify_id):
    return music_df[music_df.spotify_id == spotify_id]["title"].values[0]

music_df = pd.DataFrame(get_feature_data(session))
# print(str(music_df))
# print(music_df.columns)

## 노래 확인용
music_features = music_df[['spotify_id', 'title', 'feature_acousticness', 'feature_danceability', 'feature_energy']].values
print(music_features)