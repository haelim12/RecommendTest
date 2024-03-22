import pandas as pd
import matplotlib.pyplot as plt

from data import Session
from model.track import Track

session = Session()

# 데이터베이스에서 특성 데이터 가져오기
def get_feature_data(session):
    result = session.query(Track.feature_acousticness, Track.feature_danceability, Track.feature_energy).all()
    return result

# 특성값 분포 분석 및 출력
def analyze_feature_distribution(feature_data):
    # 데이터프레임 생성
    df = pd.DataFrame(feature_data, columns=['acousticness', 'danceability', 'energy'])

    # 특성값의 요약 통계 계산
    feature_summary = df.describe()

    # 특성값의 분포 출력
    print("--- Feature Distribution ---")
    print("Summary Statistics:")
    print(feature_summary)

    # 히스토그램 그리기
    plt.figure(figsize=(15, 5))
    for i, feature in enumerate(['acousticness', 'danceability', 'energy'], start=1):
        plt.subplot(1, 3, i)
        plt.hist(df[feature], bins=20, color='skyblue', edgecolor='black')
        plt.title(f'{feature.capitalize()} Distribution')
        plt.xlabel(feature.capitalize())
        plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

# 특성 데이터 가져오기
feature_data = get_feature_data(session)

# 특성값 분포 분석 및 출력
analyze_feature_distribution(feature_data)

