import pandas as pd

# 데이터 로드
file_path = '셔틀버스만족도.csv'
df = pd.read_csv(file_path)

# 데이터프레임의 컬럼 이름 확인
print("데이터프레임의 컬럼 이름:")
print(df.columns)

# 호서대학교 학생들만 필터링
hoseo_df = df[df['소속 대학교'] == '호서대']

# 문자열을 숫자로 매핑하는 함수 정의
def map_satisfaction(value):
    mapping = {
        '매우 만족한다.': 5,
        '만족한다.': 4,
        '보통이다': 3,
        '만족하지않는다.': 2,
        '매우 만족하지 않는다.': 1  # 0이 아닌 1로 수정
    }
    return mapping.get(value, 0)

# 컬럼 타입 변환
def convert_range_to_mean(value):
    value = value.replace('원', '').replace('(현재)', '').replace(',', '').strip()
    if '무료' in value:
        return 0.0
    if '-' in value:
        start, end = map(int, value.split('-'))
        return (start + end) / 2
    if 'or' in value:
        options = list(map(int, value.split('or')))
        return sum(options) / len(options)
    return float(value)

# 전처리 과정 디버깅용 출력 추가
print("Before conversion:")
print(hoseo_df['셔틀버스 이용 만족도'].unique())

hoseo_df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'] = hoseo_df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].astype(str).str.extract('(\d+)').astype(float)
hoseo_df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'] = hoseo_df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].astype(str).apply(convert_range_to_mean)

# 만족도를 숫자로 변환
hoseo_df['셔틀버스 이용 만족도 숫자'] = hoseo_df['셔틀버스 이용 만족도'].apply(map_satisfaction)

print("After conversion:")
print(hoseo_df['셔틀버스 이용 만족도 숫자'].unique())

# 만족도 변환 후 데이터 확인
print(hoseo_df[['셔틀버스 이용 만족도', '셔틀버스 이용 만족도 숫자']])

# 기본 통계 분석
summary_stats = hoseo_df.describe(include='all')
print(summary_stats)

# 주요 불편 사항 분석
inconvenience_analysis = hoseo_df['셔틀 버스 이용 중 불편한 점'].value_counts(normalize=True) * 100
print(inconvenience_analysis)

# 만족도 분석
satisfaction_mean = hoseo_df['셔틀버스 이용 만족도 숫자'].mean()
print(f'평균 만족도: {satisfaction_mean}')

# 셔틀버스 요금 분석
bus_fee_mean = hoseo_df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].mean()
print(f'평균 적절한 셔틀버스 요금: {bus_fee_mean}원')

# 이용 빈도 분석
usage_frequency = hoseo_df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].value_counts(normalize=True) * 100
print(usage_frequency)

# 요약 결과 작성
summary_results = {
    "전체 만족도": f"평균 {satisfaction_mean:.1f}점",
    "주요 불편 사항": inconvenience_analysis.idxmax(),
    "적절한 셔틀버스 요금": f"평균 {bus_fee_mean:.0f}원",
    "주 3회 이상 이용 비율": f"{usage_frequency[3:].sum():.1f}%",
    "셔틀버스 증설 필요성": f"{hoseo_df['셔틀버스 혼잡 시간 버스 증설 필요도'].value_counts(normalize=True).get(1, 0) * 100:.1f}% 응답"
}

print(summary_results)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

# 데이터 로드
file_path = '셔틀버스만족도.csv'
df = pd.read_csv(file_path)

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우 시스템의 경우
# font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 리눅스 시스템의 경우

font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터프레임의 컬럼 이름 확인
print("데이터프레임의 컬럼 이름:")
print(df.columns)

# 그래프 생성 함수
def plot_experience(data, column, title):
    counts = data[column].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('응답 수')
    plt.show()

# 전체 데이터 시각화
plot_experience(df, '시간표 대로 셔틀 버스가 안온 경험 횟수(기준:최근 1개월 동안) *10회 이상일 경우 기타에 적어주세요', '셔틀 버스가 안온 경험 횟수 (전체)')
plot_experience(df, '버스 줄 문제로 버스를 타지 못한 경험 횟수(기준:최근 1개월 동안)  *10회 이상일 경우 기타에 적어주세요', '버스를 타지 못한 경험 횟수 (전체)')
plot_experience(df, '막차 운영시간 적합한 시간대', '막차 운영시간 적합성 (전체)')

# 호서대 데이터 필터링
hoseo_df = df[df['소속 대학교'] == '호서대']

# 호서대 데이터 시각화
plot_experience(hoseo_df, '시간표 대로 셔틀 버스가 안온 경험 횟수(기준:최근 1개월 동안) *10회 이상일 경우 기타에 적어주세요', '셔틀 버스가 안온 경험 횟수 (호서대)')
plot_experience(hoseo_df, '버스 줄 문제로 버스를 타지 못한 경험 횟수(기준:최근 1개월 동안)  *10회 이상일 경우 기타에 적어주세요', '버스를 타지 못한 경험 횟수 (호서대)')
plot_experience(hoseo_df, '막차 운영시간 적합한 시간대', '막차 운영시간 적합성 (호서대)')

# 타 대학 데이터 필터링
non_hoseo_df = df[df['소속 대학교'] != '호서대']

# 타 대학 데이터 시각화
plot_experience(non_hoseo_df, '시간표 대로 셔틀 버스가 안온 경험 횟수(기준:최근 1개월 동안) *10회 이상일 경우 기타에 적어주세요', '셔틀 버스가 안온 경험 횟수 (타 대학)')
plot_experience(non_hoseo_df, '버스 줄 문제로 버스를 타지 못한 경험 횟수(기준:최근 1개월 동안)  *10회 이상일 경우 기타에 적어주세요', '버스를 타지 못한 경험 횟수 (타 대학)')
plot_experience(non_hoseo_df, '막차 운영시간 적합한 시간대', '막차 운영시간 적합성 (타 대학)')

