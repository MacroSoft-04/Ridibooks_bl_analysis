import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = SRC_DIR.parent
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
BASE_DIR = SRC_DIR.parent
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SAVE_DIR = OUTPUT_DIR / "top_20_keyword.png"

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(DATA_DIR / "ridi_w1_dataset.csv")

banned_words = ["평점", "무료"]

all_keywords = []

for item in df["keywords"]:
    if isinstance(item, str):
        words = item.split(",")
        for w in words:
            clean_word = w.strip()
            if not clean_word:
                continue
            is_banned = False
            for ban in banned_words:
                if ban in clean_word:
                    is_banned = True
                    break
            if not is_banned:
                all_keywords.append(clean_word)

count_result = Counter(all_keywords)
top_20 = count_result.most_common(20)
result_df = pd.DataFrame(top_20, columns=["키워드", "등장횟수"])

plt.figure(figsize=(12, 8))

sns.barplot(data=result_df, x="등장횟수", y="키워드", palette="Spectral")

plt.title("리디북스 BL 소설 인기 키워드 Top 20", fontsize=20)
plt.xlabel("작품 수", fontsize=14)
plt.grid(axis="x", linestyle="--", alpha=0.6)

plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")

print("[Top 10 카워드 랭킹]")
for i, (word, count) in enumerate(top_20[:10]):
    print(f"{i+1}위: {word} ({count}개)")
