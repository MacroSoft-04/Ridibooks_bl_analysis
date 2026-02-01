import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

plt.rc('font', family = 'AppleGothic')
plt.rcParams['axes.unicode_minus']=False

weekly_df = pd.read_csv('ridi_m_dataset_rank.csv')
monthly_df = pd.read_csv('ridi_w2_dataset_rank.csv')

try:
    all_keywords = list(weekly_df['keywords']) + list(monthly_df['keywords'])
except NameError:
    print("데이터가 없습니다.")
    all_keywords = []

banned_words = ['평점', '별점', '리뷰', '개이상', '기다리면무료', '독점', '대여', '연재', '완결', '연재중', '단행본']

def count_keywords(keyword_list):
    all_words = []
    for line in keyword_list:
        if isinstance(line, str):
            words = line.split(',')
            for w in words:
                clean_w=w.strip()
                if not clean_w: continue

                is_banned=False
                for ban in banned_words:
                    if ban in clean_w:
                        is_banned=True
                        break
                if not is_banned:
                    all_words.append(clean_w)
    return Counter(all_words)

total_counter = count_keywords(all_keywords)

rival_pairs = [
    ('능력수','순진수'),
    ('상처수', '다정수'),
    ('집착공','다정공'),
    ('미인수', '미남수'),
    ('미인공', '미남공'),
    ('현대물', '판타지물'),
    ('강공', '절륜공'),
    ('연하공', '연상공'),
    ('순정공', '계략공')
]

match_data=[]
for left, right in rival_pairs:
    left_score = total_counter[left]
    right_score = total_counter[right]

    if left_score == 0 and right_score == 0:
        continue

    match_data.append({
        'Left':left,
        'Right':right,
        'Left_Score': left_score,
        'Right_Score': right_score,
        'Total': left_score + right_score
    })

df_match = pd.DataFrame(match_data)

plt.figure(figsize=(12, 10))

y_pos = range(len(df_match))

plt.barh(y_pos, -df_match['Left_Score'], color='#ff7675', height=0.6, label='Left Win')
plt.barh(y_pos,df_match['Right_Score'], color='#74b9ff', height=0.6, label='Right Win')

plt.axvline(0, color = 'gray', linewidth = 0.5, linestyle = '--')

for i, row in df_match.iterrows():
    plt.text(-row['Left_Score'] - 3, i, f"{row['Left']}({row['Left_Score']})",
             va = 'center', ha = 'right', fontsize = 12, fontweight = 'bold', color = '#d63031')
    plt.text(row['Right_Score']+3, i, f"({row['Right_Score']}){row['Right']}",
             va='center', ha='left', fontsize=12, fontweight='bold', color='#0984e3')
    plt.text(0, i, "VS", va='center', ha='center', fontsize=9, color='gray', alpha=0.7)

plt.title('키워드 라이벌 매치', fontsize=20)
plt.xlabel('작품 수 (건)', fontsize = 12)
plt.yticks([])
plt.grid(axis='x', linestyle='--', alpha=0.3)

ticks = plt.xticks()[0]
plt.xticks(ticks, [str(abs(int(t)))for t in ticks])

plt.tight_layout()
plt.show()