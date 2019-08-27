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
ttt = pd.read_csv('영화-지무비.csv',engine='python',encoding='utf-8-sig')
like_ls = []
view_ls = []
unlike_ls = []
comment_ls = []
date_ls = []
for i in range(len(ttt)):
    if '천' in ttt['like'].iloc[i]:
        a = ''.join(re.findall('[0-9]', ttt['like'].iloc[i]))
        if len(a) == 2:
            b = a + '00'
        else:
            b = a + '000'
    elif '만' in ttt['like'].iloc[i]:
        b = ''.join(re.findall('[0-9]', ttt['like'].iloc[i])) + '000'
    else:
        b = ttt['like'].iloc[i]
    like_ls.append(b)

    if '천' in ttt['unlike'].iloc[i]:
        aa = ''.join(re.findall('[0-9]', ttt['unlike'].iloc[i]))
        if len(aa) == 2:
            bb = aa + '00'
        else:
            bb = aa + '000'
    elif '만' in ttt['unlike'].iloc[i]:
        bb = ''.join(re.findall('[0-9]', ttt['unlike'].iloc[i])) + '000'
    else:
        bb = ttt['unlike'].iloc[i]
    unlike_ls.append(bb)

    view0 = ''.join(re.findall('[0-9]', ttt['view'].iloc[i]))
    view_ls.append(view0)

    comment0 = ''.join(re.findall('[0-9]', ttt['comment'].iloc[i]))
    comment_ls.append(comment0)

    date0 = ''.join(re.findall('[.0-9]', ttt['date'].iloc[i]))
    date_ls.append(date0[:-1])

ttt['like'] = like_ls
ttt['view'] = view_ls
ttt['comment'] = comment_ls
ttt['date'] = date_ls
ttt['unlike'] = unlike_ls

ttt['view'] = ttt['view'].astype('float64')
ttt['view'].mean()
ttt[ttt['view']>=428012]

ttt2 = ttt[ttt['like']!='좋아요']
ttt2 = ttt2[ttt2['comment']!='']
ttt2['view'] = ttt2['view'].astype('float64')
ttt2['like'] = ttt2['like'].astype('float64')
ttt2['unlike'] = ttt2['unlike'].astype('float64')
ttt2['comment'] = ttt2['comment'].astype('float64')
ttt2[['view','like','comment']].corr()
# print(ttt2[['view','like','comment']].corr())
ttt2.to_csv('영화-지무비(전처리).csv', encoding='utf-8-sig', index= False)
# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib import font_manager, rc
# import matplotlib
#
# heat = ttt2[['view','like','comment']].corr()
# sns.heatmap(heat,annot=True)
# plt.show()
