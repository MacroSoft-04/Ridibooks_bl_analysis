import pandas as pd
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = SRC_DIR.parent
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"

df = pd.read_csv(DATA_DIR / "ridi_m_dataset.csv")
total_count = len(df)

is_ongoing = df["keywords"].str.contains("연재중", na=False)
is_completed = df["keywords"].str.contains("연재완결", na=False)

count_ongoing = is_ongoing.sum()
count_completed = is_completed.sum()

others_df = df[~is_ongoing & ~is_completed]
count_others = len(others_df)

print(f"[데이터 검증 리포트]")
print(f"-----------------------")
print(f"1. 전체 수집된 작품 수 : {total_count}개")
print(f"2. '연재중' 키워드 포함 : {count_ongoing}개")
print(f"3. '연재완결' 키워드 포함: {count_completed}개")
print(f"-----------------------")
print(f"검증 합계(연재중 + 연재 완결): {count_ongoing + count_completed}개")

if (count_ongoing + count_completed) == total_count:
    print(f"결과 : 누락된 데이터가 없습니다.")
else:
    diff = total_count - (count_ongoing + count_completed)
    print(f"결과 : {diff}개의 작품이 분류되지 않았습니다")

    if count_others > 0:
        print("\n[분류 안 된 작품들(Others) 확인]")
        print(others_df[["title", "keywords"]].head(10))
