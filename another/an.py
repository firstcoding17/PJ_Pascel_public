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
import seaborn as sns
import matplotlib.pyplot as plt

# 셔틀버스 이용 빈도와 만족도의 관계
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)', hue='셔틀버스 이용 만족도')
plt.title('셔틀버스 이용 빈도와 만족도의 관계')
plt.xlabel('일주일 셔틀버스 이용 횟수')
plt.ylabel('학생 수')
plt.legend(title='만족도')
plt.show()

# 셔틀버스 이용 시간대와 혼잡도의 관계
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='셔틀 버스 이용 혼잡 시간대', hue='셔틀버스 혼잡 시간 버스 증설 필요도')
plt.title('셔틀버스 이용 시간대와 혼잡도의 관계')
plt.xlabel('혼잡 시간대')
plt.ylabel('응답 수')
plt.legend(title='증설 필요도')
plt.xticks(rotation=45)
plt.show()

# 셔틀버스 요금과 만족도의 관계
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='적절한 셔틀버스 요금은 얼마인가요?(단위 원)', hue='셔틀버스 이용 만족도')
plt.title('적절한 셔틀버스 요금과 만족도의 관계')
plt.xlabel('적절한 셔틀버스 요금 (원)')
plt.ylabel('학생 수')
plt.legend(title='만족도')
plt.show()

# 셔틀버스 증설 필요도와 만족도의 관계
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='셔틀버스 혼잡 시간 버스 증설 필요도', hue='셔틀버스 이용 만족도')
plt.title('셔틀버스 증설 필요도와 만족도의 관계')
plt.xlabel('증설 필요도')
plt.ylabel('응답 수')
plt.legend(title='만족도')
plt.show()

# 주요 불편 사항과 만족도의 관계
plt.figure(figsize=(12, 6))
sns.countplot(data=df, y='셔틀 버스 이용 중 불편한 점', hue='셔틀버스 이용 만족도')
plt.title('셔틀버스 이용 중 불편한 점과 만족도의 관계')
plt.xlabel('응답 수')
plt.ylabel('불편한 점')
plt.legend(title='만족도')
plt.show()

