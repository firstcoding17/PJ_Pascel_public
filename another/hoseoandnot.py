import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 데이터 로드
file_path = r'셔틀버스만족도.csv'
df = pd.read_csv(file_path)

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우 시스템의 경우
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터프레임의 컬럼 이름 확인
print(df.columns)

# 컬럼 타입 변환 (문자열로 변환 후 숫자 추출)
df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'] = df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].astype(str).str.extract('(\d+)').astype(int)
df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'] = df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].astype(str).str.replace('원', '').astype(int, errors='ignore')

# 호서대와 호서대가 아닌 데이터로 나누기
hoseo_df = df[df['소속 대학교'] == '호서대']
non_hoseo_df = df[df['소속 대학교'] != '호서대']

# 학교 비중 시각화
school_distribution = df['소속 대학교'].value_counts()
plt.figure(figsize=(10, 6))
school_distribution.plot(kind='bar')
plt.title('학교 비중')
plt.xlabel('대학교')
plt.ylabel('학생 수')
plt.show()

# 호서대 셔틀버스 이용 빈도 시각화
hoseo_usage_frequency = hoseo_df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
hoseo_usage_frequency.plot(kind='bar')
plt.title('호서대 학생들의 일주일 셔틀버스 이용 빈도')
plt.xlabel('이용 횟수')
plt.ylabel('학생 수')
plt.show()

# 호서대가 아닌 셔틀버스 이용 빈도 시각화
non_hoseo_usage_frequency = non_hoseo_df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
non_hoseo_usage_frequency.plot(kind='bar')
plt.title('호서대가 아닌 학생들의 일주일 셔틀버스 이용 빈도')
plt.xlabel('이용 횟수')
plt.ylabel('학생 수')
plt.show()

# 호서대 셔틀버스 이용 만족도 시각화
hoseo_satisfaction_distribution = hoseo_df['셔틀버스 이용 만족도'].value_counts()
plt.figure(figsize=(10, 6))
hoseo_satisfaction_distribution.plot(kind='bar')
plt.title('호서대 학생들의 셔틀버스 이용 만족도')
plt.xlabel('만족도')
plt.ylabel('학생 수')
plt.show()

# 호서대가 아닌 셔틀버스 이용 만족도 시각화
non_hoseo_satisfaction_distribution = non_hoseo_df['셔틀버스 이용 만족도'].value_counts()
plt.figure(figsize=(10, 6))
non_hoseo_satisfaction_distribution.plot(kind='bar')
plt.title('호서대가 아닌 학생들의 셔틀버스 이용 만족도')
plt.xlabel('만족도')
plt.ylabel('학생 수')
plt.show()

# 호서대 적절한 셔틀버스 요금 시각화
hoseo_bus_fee = hoseo_df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
hoseo_bus_fee.plot(kind='bar')
plt.title('호서대 학생들의 적절한 셔틀버스 요금')
plt.xlabel('요금 (원)')
plt.ylabel('학생 수')
plt.show()

# 호서대가 아닌 적절한 셔틀버스 요금 시각화
non_hoseo_bus_fee = non_hoseo_df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
non_hoseo_bus_fee.plot(kind='bar')
plt.title('호서대가 아닌 학생들의 적절한 셔틀버스 요금')
plt.xlabel('요금 (원)')
plt.ylabel('학생 수')
plt.show()

# 호서대 셔틀버스 혼잡 시간 시각화
hoseo_congestion_time = hoseo_df['셔틀 버스 이용 혼잡 시간대'].value_counts()
plt.figure(figsize=(10, 6))
hoseo_congestion_time.plot(kind='bar')
plt.title('호서대 학생들의 셔틀버스 이용 혼잡 시간대')
plt.xlabel('혼잡 시간대')
plt.ylabel('응답 수')
plt.show()

# 호서대가 아닌 셔틀버스 혼잡 시간 시각화
non_hoseo_congestion_time = non_hoseo_df['셔틀 버스 이용 혼잡 시간대'].value_counts()
plt.figure(figsize=(10, 6))
non_hoseo_congestion_time.plot(kind='bar')
plt.title('호서대가 아닌 학생들의 셔틀버스 이용 혼잡 시간대')
plt.xlabel('혼잡 시간대')
plt.ylabel('응답 수')
plt.show()

# 호서대 셔틀버스 증설 필요도 시각화
hoseo_expansion_need = hoseo_df['셔틀버스 혼잡 시간 버스 증설 필요도'].value_counts()
plt.figure(figsize=(10, 6))
hoseo_expansion_need.plot(kind='bar')
plt.title('호서대 학생들의 셔틀버스 증설 필요도')
plt.xlabel('증설 필요도')
plt.ylabel('응답 수')
plt.show()

# 호서대가 아닌 셔틀버스 증설 필요도 시각화
non_hoseo_expansion_need = non_hoseo_df['셔틀버스 혼잡 시간 버스 증설 필요도'].value_counts()
plt.figure(figsize=(10, 6))
non_hoseo_expansion_need.plot(kind='bar')
plt.title('호서대가 아닌 학생들의 셔틀버스 증설 필요도')
plt.xlabel('증설 필요도')
plt.ylabel('응답 수')
plt.show()

# 호서대 셔틀버스 이용 중 불편한 점 시각화
hoseo_inconvenience = hoseo_df['셔틀 버스 이용 중 불편한 점'].value_counts()
plt.figure(figsize=(10, 6))
hoseo_inconvenience.plot(kind='bar')
plt.title('호서대 학생들의 셔틀버스 이용 중 불편한 점')
plt.xlabel('불편한 점')
plt.ylabel('응답 수')
plt.show()

# 호서대가 아닌 셔틀버스 이용 중 불편한 점 시각화
non_hoseo_inconvenience = non_hoseo_df['셔틀 버스 이용 중 불편한 점'].value_counts()
plt.figure(figsize=(10, 6))
non_hoseo_inconvenience.plot(kind='bar')
plt.title('호서대가 아닌 학생들의 셔틀버스 이용 중 불편한 점')
plt.xlabel('불편한 점')
plt.ylabel('응답 수')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 생성
data = {
    '대학교': ['호서대', '호서대', '호서대', '호서대', '호서대', '호서대', '호서대', '호서대', '호서대', '호서대',
              '호서대', '호서대', '호서대', '호서대', '호서대', '호서대', '순천향대', '선문대', '선문대', '선문대',
              '선문대', '선문대', '선문대', '선문대', '선문대', '선문대', '선문대', '선문대', '선문대', '선문대',
              '호서대', '호서대', '호서대', '호서대', '호서대', '호서대', '선문대', '선문대'],
    '이용 횟수': ['0번', '7회 ~ 8회', '1회 ~ 2회', '1회 ~ 2회', '7회 ~ 8회', '7회 ~ 8회', '7회 ~ 8회', '7회 ~ 8회', '1회 ~ 2회', '1회 ~ 2회',
              '3회 ~ 4회', '1회 ~ 2회', '3회 ~ 4회', '3회 ~ 4회', '9회 이상', '9회 이상', '1회 ~ 2회', '9회 이상', '5회 ~ 6회', '9회 이상',
              '1회 ~ 2회', '1회 ~ 2회', '3회 ~ 4회', '1회 ~ 2회', '7회 ~ 8회', '5회 ~ 6회', '7회 ~ 8회', '3회 ~ 4회', '3회 ~ 4회', '7회 ~ 8회',
              '9회 이상', '7회 ~ 8회', '9회 이상', '5회 ~ 6회', '9회 이상', '5회 ~ 6회', '1회 ~ 2회', '1회 ~ 2회'],
    '셔틀버스 요금': ["1000", "800", "500원", "1000원", "1000", "500-1000", "1000", "800", "1300", "500",
                "무료", "1200", "500원", "700원", "500", "1000", "(현재) 무료", "1000", "1000", "무료",
                "1000", "500원", "0", "0", "1000 or 500원", "1000", "500", "무료", "1500", "1000원",
                "800", "700", "1000", "1000", "1000", "1000", "1,000원", "1000원"]
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 셔틀버스 요금을 숫자로 변환하는 함수 정의
def convert_to_mean(value):
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

# 셔틀버스 요금을 숫자로 변환
df['셔틀버스 요금'] = df['셔틀버스 요금'].apply(convert_to_mean)

# 전체 데이터 박스플롯 및 평균 출력
plt.figure(figsize=(10, 6))
sns.boxplot(x='셔틀버스 요금', data=df)
plt.title('전체 셔틀버스 요금 분포')
plt.show()
overall_mean = df['셔틀버스 요금'].mean()
print(f'전체 평균 셔틀버스 요금: {overall_mean:.2f}원')

# 호서대 데이터 필터링
hoseo_df = df[df['대학교'] == '호서대']

# 호서대 박스플롯 및 평균 출력
plt.figure(figsize=(10, 6))
sns.boxplot(x='셔틀버스 요금', data=hoseo_df)
plt.title('호서대 셔틀버스 요금 분포')
plt.show()
hoseo_mean = hoseo_df['셔틀버스 요금'].mean()
print(f'호서대 평균 셔틀버스 요금: {hoseo_mean:.2f}원')

# 타 대학 데이터 필터링
non_hoseo_df = df[df['대학교'] != '호서대']

# 타 대학 박스플롯 및 평균 출력
plt.figure(figsize=(10, 6))
sns.boxplot(x='셔틀버스 요금', data=non_hoseo_df)
plt.title('타 대학 셔틀버스 요금 분포')
plt.show()
non_hoseo_mean = non_hoseo_df['셔틀버스 요금'].mean()
print(f'타 대학 평균 셔틀버스 요금: {non_hoseo_mean:.2f}원')
