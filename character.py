import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus']=False

try:
    keyword_map = pd.read_csv('ridi_keyword.csv')

    keyword_map['카테고리']=keyword_map['카테고리'].str.strip()
    keyword_map['키워드']=keyword_map['키워드'].str.strip()

    gong_list = set(keyword_map[keyword_map['카테고리']=='인물(공)']['키워드'])
    soo_list = set(keyword_map[keyword_map['카테고리']=='인물(수)']['키워드'])

    print(f"기준 파일 로드 완료: 공 키워드 {len(gong_list)}개 / 수 키워드 {len(soo_list)}개 확보")

except FileNotFoundError:
    print("'ridi_keysord.csv'파일을 찾을 수 없음. 같은 폴더에 있는지 확인 요망.")
    exit()

try:
    weekly_original = pd.read_csv('ridi_w2_dataset_rank.csv')
    monthly_original=pd.read_csv('ridi_m_dataset_rank.csv')
except FileNotFoundError:
    print("랭킹 데이터 파일을 찾을 수 없습니다.")
    exit()

weekly_df = weekly_original[weekly_original['keywords'].str.contains('연재중', na=False)]
monthly_df = monthly_original[monthly_original['keywords'].str.contains('연재중', na=False)]

def get_filtered_counts(df_column, target_list):
    keywords=[]
    for item in df_column:
        if isinstance(item, str):
            words = item.split(',')
            for w in words:
                clean_w=w.strip()
                if clean_w in target_list:
                    keywords.append(clean_w)
    return Counter(keywords)

def make_plot_data(target_list):
    w_counts = get_filtered_counts(weekly_df['keywords'], target_list)
    m_counts = get_filtered_counts(monthly_df['keywords'], target_list)

    found_keywords = set(w_counts.keys())|set(m_counts.keys())

    data = []
    for word in found_keywords:
        w = w_counts[word]
        m = m_counts[word]
        total = w + m
        data.append({'Keyword':word, 'Weekly':w, 'Monthly':m, 'Total':total})

    if not data:
        return pd.DataFrame()
    
    return pd.DataFrame(data).sort_values(by='Total', ascending=False).head(20)

df_gong = make_plot_data(gong_list)
df_soo = make_plot_data(soo_list)

fig, axes = plt.subplots(1, 2, figsize = (20, 12))

if not df_gong.empty:
    df_gong=df_gong.set_index('Keyword').iloc[::-1]
    ax1 = df_gong[['Monthly','Weekly']].plot(kind='barh', stacked=True,
                                             ax=axes[0], color=['#2d3436', '#d63031'])
    axes[0].set_title('인물(공) 트렌드 Top 20', fontsize=20, fontweight='bold')
    axes[0].set_xlabel('등장 횟수', fontsize=12)
    axes[0].grid(axis='x', linestyle='--', alpha=0.3)

    for p in ax1.patches:
        width = p.get_width()
        if width >3:
            ax1.text(p.get_x()+width/2, p.get_y()+p.get_height()/2,
                     f'{int(width)}', ha = 'center', va='center', color='white', fontsize=10, fontweight='bold')
else:
    axes[0].text(0.5, 0.5, '데이터 없음', ha = 'center', va = 'center')

if not df_soo.empty:
    df_soo = df_soo.set_index('Keyword').iloc[::-1]
    ax2 = df_soo[['Monthly', 'Weekly']].plot(kind='barh', stacked=True,
                                             ax = axes[1], color=['#2d3436', '#0984e3'])
    axes[1].set_title('인물(수) 트렌드 top20', fontsize = 20, fontweight = 'bold')
    axes[1].set_xlabel('등장 횟수', fontsize=12)
    axes[1].grid(axis='x', linestyle='--', alpha=0.3)

    for p in ax2.patches:
        width = p.get_width()
        if width > 3:
            ax2.text(p.get_x() + width/2, p.get_y() + p.get_height()/2,
                     f'{int(width)}', ha='center', va='center', color='white', fontsize=10, fontweight='bold')
            
else:
    axes[1].text(0.5, 0.5, '데이터 없음', ha = 'center', va = 'center')

axes[0].legend(['월간 누적(Base)', '주간 반영(Trend)'], loc='lower right')
axes[1].legend(['월간 누적(Base)', '주간 반영(Trend)'], loc='lower right')

plt.tight_layout()
plt.show()