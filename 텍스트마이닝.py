import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Twitter
import re
import numpy as np
from collections import Counter

muk = pd.read_csv('먹방(전처리).csv', encoding='utf-8')
a = muk['title']

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

#분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')

comment_list = []
for i in range(len(muk)):
    comment_list.append(muk['title'].iloc[i])

comment_result = []

for i in comment_list:
    tokens = re.sub(emoji_pattern,"",i)
    tokens = re.sub(han,"",tokens)
    comment_result.append(tokens)

comment_result = pd.DataFrame(comment_result, columns=["title"])

# print(comment_result)


def get_noun(comment_txt):
    twitter = Twitter()
    noun = []

    if len(comment_txt) > 0:
        tw = twitter.pos(comment_txt)
        for i, j in tw:
            if j == 'Noun':
                noun.append(i)
    return noun


comment_result['token'] = comment_result['title'].apply(lambda x: get_noun(x))
print(comment_result.tail(5))

noun_list = []
for i in range(len(comment_result)):
    for j in range(len(comment_result['token'].iloc[i])):
        noun_list.append(comment_result['token'].iloc[i][j])

counts = Counter(noun_list)
tags = counts.most_common(30)
print(tags)
test = pd.DataFrame({'word': [],
                     'count': []})

for i in range(len(tags)):
    word = tags[i][0]
    count = tags[i][1]
    insert_data = pd.DataFrame({'word': [word],
                                'count': [count]})
    test = test.append(insert_data)

test.index = range(len(test))

index = np.arange(len(test))
plt.bar(index, test['count'].tolist())
plt.xlabel('word', fontsize=5)
plt.ylabel('count', fontsize=5)
plt.xticks(index, test['word'].tolist(), fontsize=5, rotation=30)
plt.title('단어 빈도수 시각화')
plt.show()

wc = WordCloud(font_path='C:/Users/user/AppData/Local/Microsoft/Windows/Fonts/KoPub Dotum Bold.ttf', background_color='white', width=800,
                   height=600)

print(dict(tags))
cloud = wc.generate_from_frequencies(dict(tags))
plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()

