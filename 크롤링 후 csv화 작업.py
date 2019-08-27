import requests # 웹 페이지 소스를 얻기 위한 패키지(기본 내장 패키지이다.)
from bs4 import BeautifulSoup # 웹 페이지 소스를 얻기 위한 패키지, 더 간단히 얻을 수 있다는 장점이 있다고 한다.
from datetime import datetime                                # (!pip install beautifulsoup4 으로 다운받을 수 있다.)
import pandas as pd # 데이터를 처리하기 위한 가장 기본적인 패키지
import time # 사이트를 불러올 때, 작업 지연시간을 지정해주기 위한 패키지이다. (사이트가 늦게 켜지면 에러가 발생하기 때문)
import urllib.request #
from selenium.webdriver import Chrome
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt

start_url  = 'http://www.youtube.com'
delay=3
browser = Chrome("C:/users/user/downloads/chromedriver.exe")
browser.implicitly_wait(delay)

browser.get(start_url)


browser.find_elements_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input')[0].click()

browser.find_elements_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input')[0].send_keys('보람TOY')

browser.find_elements_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input')[0].send_keys(Keys.RETURN)

browser.find_elements_by_xpath('//*[@class="yt-simple-endpoint style-scope ytd-channel-renderer"]/div[2]/h3/span')[0].click()

browser.find_element_by_xpath('//*[@class="scrollable style-scope paper-tabs"]/paper-tab[2]').click()

time.sleep(3)
body = browser.find_element_by_tag_name('body')

num_of_pagedowns = 20
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    num_of_pagedowns -= 1

html0 = browser.page_source

html = BeautifulSoup(html0,'html.parser')

video_ls=html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})

b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})

len(b.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'}))

tester_url = []
for i in range(len(video_ls)):
    url = start_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
    tester_url.append(url)

print(tester_url)

browser.get(tester_url[2])
body = browser.find_element_by_tag_name('body')
num_of_pagedowns = 2
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    num_of_pagedowns -= 1

time.sleep(3)

soup0 = browser.page_source
soup = BeautifulSoup(soup0,'html.parser')
info1 = soup.find('div',{'id':'info-contents'})
comment = soup.find('yt-formatted-string',{'class':'count-text style-scope ytd-comments-header-renderer'}).text
title = info1.find('h1',{'class':'title style-scope ytd-video-primary-info-renderer'}).text
view =info1.find('yt-view-count-renderer',{'class':'style-scope ytd-video-primary-info-renderer'}).find_all('span')[0].text
like = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[0].text
unlike = info1.find('div',{'id':'top-level-buttons'}).find_all('yt-formatted-string')[1].text
date = soup.find('span',{'class':'date style-scope ytd-video-secondary-info-renderer'}).text
video_info = pd.DataFrame({'title':[],
                          'view':[],
                          'like':[],
                          'unlike':[],
                          'comment':[],
                          'date':[]})

for i in range(95, len(tester_url)):
    browser.get(tester_url[i])
    time.sleep(1.5)

    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    num_of_pagedowns = 2
    # 10번 밑으로 내리는 것
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1

    time.sleep(2)

    soup0 = browser.page_source
    time.sleep(1.5)
    soup = BeautifulSoup(soup0, 'html.parser')

    info1 = soup.find('div', {'id': 'info-contents'})

    try:
        comment = soup.find('yt-formatted-string',
                            {'class': 'count-text style-scope ytd-comments-header-renderer'}).text
    except:
        comment = '댓글x'
    title = info1.find('h1', {'class': 'title style-scope ytd-video-primary-info-renderer'}).text
    view = \
    info1.find('yt-view-count-renderer', {'class': 'style-scope ytd-video-primary-info-renderer'}).find_all('span')[
        0].text
    like = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[0].text
    unlike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
    date = soup.find('span', {'class': 'date style-scope ytd-video-secondary-info-renderer'}).text

    insert_data = pd.DataFrame({'title': [title],
                                'view': [view],
                                'like': [like],
                                'unlike': [unlike],
                                'comment': [comment],
                                'date': [date]})

    video_info = video_info.append(insert_data)

video_info.index = range(len(video_info))
video_info.index = range(len(video_info))
video_info.to_csv('키즈-보람TOY.csv', encoding='utf-8-sig')

