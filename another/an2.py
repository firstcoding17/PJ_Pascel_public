import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

# 데이터 로드
file_path = '셔틀버스만족도.csv'
df = pd.read_csv(file_path)

# 데이터프레임의 컬럼 이름 확인
print(df.columns)

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우 시스템의 경우
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 범위 값을 처리하는 함수 정의
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

# 컬럼 타입 변환
df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'] = df['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)'].astype(str).str.extract('(\d+)').astype(float)
df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'] = df['적절한 셔틀버스 요금은 얼마인가요?(단위 원)'].astype(str).apply(convert_range_to_mean)

# 만족도를 이진 변수로 변환
df['만족도_이진'] = df['셔틀버스 이용 만족도'].apply(lambda x: 1 if x in ['만족한다', '매우 만족한다'] else 0).astype(float)

# 상관 행렬 계산
correlation_matrix = df[['일주일에 몇번 셔틀 버스를 이용하시나요?(ex: 화 수 목 학교 등교시 6회)',
                        '적절한 셔틀버스 요금은 얼마인가요?(단위 원)',
                        '만족도_이진']].corr()

# 상관 행렬 출력
print(correlation_matrix)

# 상관 행렬 시각화
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

