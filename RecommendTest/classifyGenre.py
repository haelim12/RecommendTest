import pandas as pd

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

## Step 2: 특성 선택.
features = ['feature_acousticness', 'feature_danceability', 'feature_energy']

for feature in features:
    music_df[feature] = music_df[feature].fillna('')
    # print(str(music_df[feature]))

def classify_genre(acousticness, danceability, energy):
    if danceability >= 0.727:
        return 'Dance'
    elif acousticness >= 0.171:
        return 'R&B'
    elif energy >= 0.730:
        return 'Rock'
    else:
        return 'Pop'

# 장르 할당
music_df['genre'] = music_df.apply(lambda row: classify_genre(row['feature_acousticness'], row['feature_danceability'], row['feature_energy']), axis=1)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(music_df[['title', 'genre']])