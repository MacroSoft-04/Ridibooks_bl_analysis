import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

plt.rc('font', family = 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('ridi_m_dataset.csv')

ongoing_df = df[df['keywords'].str.contains('연재중', na = False)]
print(f"분석 대상 : 전체 {len(df)}개 중 '연재중'인 {len(ongoing_df)}개 작품")
banned_words = [
    "평점", "별점", "리뷰", "개이상", "기다리면무료", "독점", "대여",
    '연재', '완결','연재중', '완결'
]

all_keywords = []

for item in ongoing_df['keywords']:
    if isinstance(item, str):
        words = item.split(',')
        for w in words:
            clean_word = w.strip()

            if not clean_word : continue

            is_banned = False
            for ban in banned_words:
                if ban in clean_word:
                    is_banned = True
                    break
            
            if not is_banned:
                all_keywords.append(clean_word)

count_result = Counter(all_keywords)
top_20 = count_result.most_common(20)
result_df = pd.DataFrame(top_20, columns = ['키워드', '등장횟수'])

plt.figure(figsize=(12, 8))
ax = sns.barplot(data = result_df, x = '등장횟수', y = '키워드', hue = '키워드', palette = 'viridis', legend=False)

for p in ax.patches:
    width = p.get_width()
    y_loc = p.get_y() + p.get_height() / 2
    if width > 0:
        ax.annotate(f'{int(p.get_width())}건', 
                    (width, y_loc), 
                    ha = 'left', va = 'center', 
                    xytext = (5, 0), 
                    textcoords= 'offset points')
        
plt.title('현재 연재 중인 작품(92개)의 핵심 트렌드 Top 20 (월간베스트)', fontsize = 18)
plt.xlabel('작품 수', fontsize = 14)
plt.ylabel('키워드', fontsize = 14)
plt.grid(axis = 'x', linestyle = '--', alpha = 0.3)

plt.show()

print("\n [실시간 연재 트렌드 Ranking]")
for i, (word, count) in enumerate(top_20[:10]):
    print(f"{i+1}위: {word} ({count}개)")