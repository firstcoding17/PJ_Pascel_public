import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc


file_path = r'셔틀버스만족도.csv'
df = pd.read_csv(file_path)


# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우 시스템의 경우
# font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 리눅스 시스템의 경우

font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


# 데이터프레임의 컬럼 이름 확인
print(df.columns)

# 컬럼 타입 변환 (문자열로 변환 후 숫자 추출)
df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'] = df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].astype(str).str.extract('(\d+)').astype(int)
df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'] = df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].astype(str).str.replace('원', '').astype(int, errors='ignore')

# 학교 비중 시각화
school_distribution = df['소속 대학교'].value_counts()
plt.figure(figsize=(10, 6))
school_distribution.plot(kind='bar')
plt.title('학교 비중')
plt.xlabel('대학교')
plt.ylabel('학생 수')
plt.show()

# 셔틀버스 이용 빈도 시각화
usage_frequency = df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
usage_frequency.plot(kind='bar')
plt.title('일주일 셔틀버스 이용 빈도')
plt.xlabel('이용 횟수')
plt.ylabel('학생 수')
plt.show()

# 셔틀버스 이용 만족도 시각화
satisfaction_distribution = df['셔틀버스 이용 만족도'].value_counts()
plt.figure(figsize=(10, 6))
satisfaction_distribution.plot(kind='bar')
plt.title('셔틀버스 이용 만족도')
plt.xlabel('만족도')
plt.ylabel('학생 수')
plt.show()

# 적절한 셔틀버스 요금 시각화
bus_fee = df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
bus_fee.plot(kind='bar')
plt.title('적절한 셔틀버스 요금')
plt.xlabel('요금 (원)')
plt.ylabel('학생 수')
plt.show()

# 셔틀버스 혼잡 시간 시각화
congestion_time = df['셔틀 버스 이용 혼잡 시간대'].value_counts()
plt.figure(figsize=(10, 6))
congestion_time.plot(kind='bar')
plt.title('셔틀버스 이용 혼잡 시간대')
plt.xlabel('혼잡 시간대')
plt.ylabel('응답 수')
plt.show()

# 셔틀버스 증설 필요도 시각화
expansion_need = df['셔틀버스 혼잡 시간 버스 증설 필요도'].value_counts()
plt.figure(figsize=(10, 6))
expansion_need.plot(kind='bar')
plt.title('셔틀버스 증설 필요도')
plt.xlabel('증설 필요도')
plt.ylabel('응답 수')
plt.show()

# 셔틀버스 이용 중 불편한 점 시각화
inconvenience = df['셔틀 버스 이용 중 불편한 점'].value_counts()
plt.figure(figsize=(10, 6))
inconvenience.plot(kind='bar')
plt.title('셔틀버스 이용 중 불편한 점')
plt.xlabel('불편한 점')
plt.ylabel('응답 수')
plt.show()

