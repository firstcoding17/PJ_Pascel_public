import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # 추가: TimeoutException 임포트
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('start-maximized') # 창 최대화
driver = webdriver.Chrome(options=chrome_options)

url = 'https://play.google.com/store/apps/details?id=com.navercorp.game.android.community&hl=ko&gl=US' #크롤링주소
driver.get(url)
wait = WebDriverWait(driver, 5)

# 리뷰 섹션 확장
try:
    spread_review = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button'))
    )
    spread_review.click()
except TimeoutException:  # 추가: TimeoutException 처리
    print("리뷰 모두 보기 버튼이 로드되지 않았습니다.")

# 모든 리뷰 수집
all_reviews = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[2]')
for i in range(10):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', all_reviews)
    time.sleep(3)

# 데이터프레임 생성
data = pd.DataFrame(columns=['리뷰', '별점'])

# 리뷰 섹션 확장
try:
    spread_review = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button'))
    )
    spread_review.click()
except TimeoutException:
    print("리뷰 모두 보기 버튼이 로드되지 않았습니다.")

# 모든 리뷰 수집
all_reviews = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[2]')
for i in range(10):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', all_reviews)
    time.sleep(3)

# 리뷰, 별점 수집
reviews_elements = driver.find_elements(By.XPATH, '//div[@class="h3YV2d"]')
stargrades_elements = driver.find_elements(By.XPATH, '//div[@class="iXRFPc"]')

# 데이터프레임에 데이터 추가
for i in range(len(reviews_elements)):
    review = reviews_elements[i].text
    stargrade = stargrades_elements[i].get_attribute('aria-label')

    data = pd.concat([data, pd.DataFrame({'리뷰': [review], '별점': [stargrade]})], ignore_index=True)

# CSV 파일로 저장
data.reset_index(inplace=True, drop=True)


data.to_csv('crawling_UXUI.csv', index=False, encoding='utf-8-sig')

















