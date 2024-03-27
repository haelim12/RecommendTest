import pandas as pd

from data import Session
from model.track import Track

session = Session()

# 특징 데이터 가져오기
def get_feature_data(session):
    result = session.query(Track.title, Track.spotify_id, Track.feature_acousticness, Track.feature_danceability, Track.feature_energy).all()
    return result

music_df = pd.DataFrame(get_feature_data(session))
# print(str(music_df))
# print(music_df.columns)

def classify_genre(acousticness, danceability, energy):
    if danceability >= 0.727:
        return 'dance'
    elif acousticness >= 0.171:
        return 'rnb'
    elif energy >= 0.730:
        return 'rock'
    else:
        return 'pop'

# 장르 할당
music_df['genre'] = music_df.apply(lambda row: classify_genre(row['feature_acousticness'], row['feature_danceability'], row['feature_energy']), axis=1)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(music_df[['title', 'genre']])