import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import urllib.request
from selenium.webdriver import Chrome
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import matplotlib
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
from konlpy.tag import Komoran

ttt = pd.read_csv('haha ha 크롤링 결과.csv',engine='python',encoding='cp949')
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
        if len(a) == 2:
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
print(ttt2[['view','like','comment']].corr())

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import matplotlib

heat = ttt2[['view','like','comment']].corr()
sns.heatmap(heat,annot=True)
plt.show()

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')
title_ls = []
for i in range(len(ttt)):
    a = re.sub(emoji_pattern, '', ttt['title'].iloc[i])

    b = re.sub(han, '', a)

    title_ls.append(b)

ttt['title'] = title_ls
twitter = Twitter()
kkma = Kkma()

noun_final = []
for text in range(len(ttt)):
    noun0=kkma.pos(ttt['title'].iloc[text])
    noun=[]
    for i,j in noun0:
        if j=='NNG':
            if i == '테스터' or i == '훈':
                pass
            else:
                noun.append(i)
    noun_final.append(noun)
ttt['token'] = noun_final
noun_ls = []
for i in range(len(ttt)):
    noun_ls0=[]
    for j in range(len(ttt['token'].iloc[i])):
        if len(ttt['token'].iloc[i][j]) == 1:
            pass
        else:
            noun_ls0.append(ttt['token'].iloc[i][j])
    noun_ls.append(list(set(noun_ls0)))

ttt['token2'] = noun_ls

print(ttt)

token_df = pd.DataFrame({'token': []})
for i in range(len(ttt)):
    insert_data = pd.DataFrame({'token': ttt['token2'].iloc[i]})
    insert_data['view'] = ttt['view'].iloc[i]

    token_df = token_df.append(insert_data)

token_df['view'] = token_df['view'].astype('float64')
token_df2 = token_df.groupby('token')['view'].sum().reset_index()
token_df2['count'] = token_df.groupby(['token']).count().reset_index()['view'].tolist()

view_count = []
for i in range(len(token_df2)):
    a = token_df2['view'].iloc[i]/token_df2['count'].iloc[i]
    view_count.append(a)
token_df2['view_count'] = view_count
print('단어별 조회수')
print('카운트 순\n',token_df2.sort_values(by='count',ascending=False).head(15))
print('조회수 순 내림차순\n',token_df2.sort_values(by='view',ascending=False).head(20))
print('조회수 순 오름차순\n',token_df2.sort_values(by='view').head(20))
print('조회수/카운트 내림차순\n',token_df2.sort_values(by='view_count',ascending=False).head(15))
print('조회수/카운트 오름차순\n',token_df2.sort_values(by='view_count').head(15))

token_df = pd.DataFrame({'token': []})
for i in range(len(ttt)):
    insert_data = pd.DataFrame({'token': ttt['token2'].iloc[i]})
    insert_data['like'] = ttt['like'].iloc[i]

    token_df = token_df.append(insert_data)

token_df = token_df[token_df['like'] != '좋아요']
token_df['like'] = token_df['like'].astype('float64')
token_df2 = token_df.groupby('token')['like'].sum().reset_index()
token_df2['count'] = token_df.groupby(['token']).count().reset_index()['like'].tolist()
view_count = []
for i in range(len(token_df2)):
    a = token_df2['like'].iloc[i]/token_df2['count'].iloc[i]
    view_count.append(a)
token_df2['like_count'] = view_count
print('키워드별 좋아요 수')
print('키워드별 좋아요 수 내림차순\n',token_df2.sort_values(by='like_count',ascending=False).head(15))
print('키워드별 좋아요 수 오름차순\n',token_df2.sort_values(by='like_count').head(15))

