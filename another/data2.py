import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 데이터 로드
file_path = '셔틀버스만족도.csv'
df = pd.read_csv(file_path)

# 데이터프레임의 컬럼 이름 확인
print(df.columns)

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우 시스템의 경우
# font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 리눅스 시스템의 경우

font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 컬럼 타입 변환
df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'] = df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].str.extract('(\d+)').astype(int)
df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'] = df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].str.replace('원', '').astype(int, errors='ignore')

# 기본 통계 분석
basic_stats = df.describe(include='all')
print("기본 통계 분석:\n", basic_stats)

# 셔틀버스 이용 빈도와 만족도 분석
usage_satisfaction = df.groupby('일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)')['셔틀버스 이용 만족도'].value_counts(normalize=True).unstack().fillna(0)
print("\n셔틀버스 이용 빈도와 만족도 분석:\n", usage_satisfaction)

# 혼잡 시간대 분석
congestion_analysis = df['셔틀 버스 이용 혼잡 시간대'].value_counts()
print("\n혼잡 시간대 분석:\n", congestion_analysis)

# 증설 필요성 분석
expansion_analysis = df['셔틀버스 혼잡 시간 버스 증설 필요도'].value_counts()
print("\n증설 필요성 분석:\n", expansion_analysis)

# 불편 사항 분석
inconvenience_analysis = df['셔틀 버스 이용 중 불편한 점'].value_counts()
print("\n불편 사항 분석:\n", inconvenience_analysis)

# 시각화 예시
plt.figure(figsize=(10, 6))
usage_satisfaction.plot(kind='bar', stacked=True)
plt.title('셔틀버스 이용 빈도와 만족도 분석')
plt.xlabel('일주일 이용 횟수')
plt.ylabel('비율')
plt.legend(title='만족도')
plt.show()

