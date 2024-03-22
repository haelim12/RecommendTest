import pandas as pd
import matplotlib.pyplot as plt

from data import Session
from model.track import Track

session = Session()

# 데이터베이스에서 특성 데이터 가져오기
def get_feature_data(session):
    result = session.query(Track.spotify_id, Track.title, Track.spotify_popularity).all()
    return result

# popularity 기준으로 노래 정렬
def sort_by_popularity(feature_data):
    music_df = pd.DataFrame(feature_data, columns=['spotify_id', 'title', 'popularity'])
    music_df = music_df.sort_values(by='popularity', ascending=False)
    return music_df


