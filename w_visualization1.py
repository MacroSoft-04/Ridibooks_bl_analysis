import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

plt.rc('font',family = 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('ridi_w_dataset.csv')

banned_words = [
    "평점", "무료"
]

all_keywords=[]

for item in df['keywords']:
    if isinstance(item, str):
        words = item.split(',')
        for w in words:
            clean_word = w.strip()
            if not clean_word: continue
            is_banned = False
            for ban in banned_words:
                if ban in clean_word:
                    is_banned = True
                    break
            if not is_banned:
                all_keywords.append(clean_word)

count_result = Counter(all_keywords)
top_20 = count_result.most_common(20)
result_df = pd.DataFrame(top_20, columns=['키워드','등장횟수'])

plt.figure(figsize=(12, 8))

sns.barplot(data = result_df, x='등장횟수', y='키워드', palette='Spectral')

plt.title('리디북스 BL 소설 인기 키워드 Top 20', fontsize = 20)
plt.xlabel('작품 수', fontsize = 14)
plt.grid(axis = 'x', linestyle= '--', alpha = 0.6)

plt.show()

print("[Top 10 카워드 랭킹]")
for i, (word, count) in enumerate(top_20[:10]):
    print(f"{i+1}위: {word} ({count}개)") 