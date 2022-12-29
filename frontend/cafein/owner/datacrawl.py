import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import datetime, timedelta


def findCafe(phone, name):
    url = f'https://m.map.naver.com/search2/searchMore.naver?query={phone}&page=1'
    response = requests.get(url)
    places = response.json()['result']['site']['list']
    for place in places:
        if place['name'] == name:
            return place['id'][1:]


def dateCal(str):
    date = str.split(" ")
    year = int(date[0][:-1])
    month = int(date[1][:-1])
    day = int(date[2][:-1])
    
    return datetime(year, month, day)


def clickMore(driver, days=90):
    now = datetime.now()

    while True: 
            try: 
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1)
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
                time.sleep(1) 
                
                date = driver.find_element(By.CSS_SELECTOR, '.eCPGL > li:nth-last-child(1) > div:nth-last-child(1) > span > span:nth-last-child(1)').text
                
                dt = dateCal(date)
                diff = (now-dt).total_seconds()//86400
                
                if diff > days: # 맨 마지막 리뷰 일자가 90일 이전이면 멈춤
                    break
                
                driver.find_element(By.CSS_SELECTOR, '.lfH3O > a').click()
                time.sleep(2)           
                
                
            except NoSuchElementException: 
                print('-더보기 버튼 모두 클릭 완료-') 
                break 


def seeDetails(driver, action):
    elements = driver.find_elements(By.CSS_SELECTOR, '.YeINN')

    for element in elements:
        more = element.find_elements(By.CSS_SELECTOR, '.ZZ4OK > a > .rvCSr')
        if len(more) > 0:
            action.move_to_element(element).perform()
            time.sleep(1)
            more[0].click()


def scrapReviews(html, datelist, reviewlist):
    dom = BeautifulSoup(html, 'lxml')

    reviews = dom.select('.YeINN > .ZZ4OK > a > span:nth-child(1)')
    dates = dom.select('.YeINN > div:nth-last-child(1) > span > span:nth-last-child(1)')

    try: 
        for date, review in zip(dates, reviews): 
            
            day = dateCal(date.text)
            text = review.text
        
            datelist.append(day)
            reviewlist.append(text)

    # 리뷰가 없는 경우        
    except NoSuchElementException: 
        print("네이버 리뷰 없음" )



def collectData(cafename, cafenum):
    cafeID = findCafe(cafenum, cafename)
    
    driver = webdriver.Chrome('./modeling/chromedriver')
    action = ActionChains(driver)

    days = []
    re = []

    finalurl = f'https://m.place.naver.com/restaurant/{cafeID}/review/visitor?reviewSort=recent'
    driver.get(finalurl)

    clickMore(driver)
    time.sleep(2)

    seeDetails(driver, action)

    html = driver.page_source

    scrapReviews(html, days, re)
    print(f'{cafename} 리뷰 수집 완료')

    driver.quit()

    df = pd.DataFrame({'date': days, 'review': re})

    now = datetime.now()
    tmp = now + timedelta(days=-90)
    condition = df.loc[df['date']>=tmp]

    condition.to_csv(f'.cafein/files/{cafename}_{now.strftime("%Y%m%d")}_raw.csv', index=False, encoding='utf-8-sig')
  
    return condition