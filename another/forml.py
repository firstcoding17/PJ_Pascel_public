'''import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('start-maximized') # 창 최대화
# chrome_options.add_argument('window-size=1920,1080') # 윈도우 사이즈 설정
# chrome_options.add_argument('headless') # 크롬 탭 띄우지 않음

driver = webdriver.Chrome(options=chrome_options)

url = 'https://play.google.com/store/apps/details?id=com.navercorp.game.android.community&hl=ko&gl=US' #크롤링주소
# 페이지 열기
driver.get(url)
# 페이지 로딩 대기
wait = WebDriverWait(driver, 5)
#YNR7H이름
#Jx4nYe평점 년도
#h3YB2d평가
# 스크롤 최하단으로 내리기
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#리뷰전체보기클릭
spread_review = driver.find_element(by=By.XPATH, value = '/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button')
spread_review = driver.execute_script("arguments[0].click()")
isTrue = spread_review.is_displayed()
if isTrue :
    driver.execute_script("arguments[0].click();", spread_review)
    time.sleep(1.5)

all_reviews = driver.find_element(by=By.XPATH, value ='//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[2]')

# 모든 리뷰 수집
all_reviews = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[2]')
for i in range(10):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', all_reviews)
    time.sleep(3)

data = pd.DataFrame(data=[], columns=['이름','리뷰','별점'])

name=driver.find_elements(by=By.XPATH, value = '//div[@class="YNR7H"]')
reviews=driver.find_elements(by=By.XPATH, value = '//div[@class="h3YV2d"]')
stargrades = driver.find_elements(by=By.XPATH, value = '//div[@class="Jx4nYe"]')

for i in range(len(reviews)):
    tmp = []
    tmp.append(name[i].text)
    tmp.append(reviews[i].text)
    tmp.append(stargrades[i].get_attribute('aria-label'))

    tmp = pd.DataFrame(data=[tmp], columns=data.columns)
    data = pd.concat([data, tmp])

print("치지직 앱 리뷰 수집 완료")

data.reset_index(inplace=True, drop=True)
data.to_csv('crawling_UXUI')
'''
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('UXUIfeedbackreview.csv')

# 각 컬럼의 1 비율 계산
percentages = df.mean() * 100

# 그래프 그리기
plt.figure(figsize=(10, 6))
percentages.plot(kind='bar', color='skyblue')
plt.title('Percentage Each Column')
plt.xlabel('Columns')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()