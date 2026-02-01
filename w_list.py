import pandas as pd
from urllib.parse import urlparse, parse_qs

df = pd.read_csv('ridi_m_dataset.csv')

def extract_real_rank(url):
    try:
        if not isinstance(url, str): return 9999
        clean_url = url.strip()
        parsed_url = urlparse(clean_url)
        query_params = parse_qs(parsed_url.query)

        if '_rdt_idx' in query_params:
            return int(query_params['_rdt_idx'][0])
        
        return 9999

    except Exception as e:
        print(F"에러 발생한 링크 : {url} / 사유: {e}")
        return 9999

print("순위 재계산 중..")
df['rank_index'] = df['link'].apply(extract_real_rank)

df_sorted = df.sort_values(by = 'rank_index', ascending=True)

df_sorted['Real_Rank'] = df_sorted['rank_index']+1

print("\n[진짜 정렬된 Top 5]")
print(df_sorted[['Real_Rank', 'title']].head(5))

print("\n[가장 마지막 순위 5개]")
print(df_sorted[['Real_Rank', 'title']].tail(5))

df_sorted.to_csv('ridi_m_dataset_rank.csv', index=False, encoding = 'utf-8-sig')
print("\n 저장 완료")