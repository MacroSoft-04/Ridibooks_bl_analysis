import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
BASE_DIR = SRC_DIR.parent
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SAVE_DIR = OUTPUT_DIR / "overlaped_monthly_weekly_best_keyword.png"

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

try:
    weekly1_df = pd.read_csv(DATA_DIR / "ridi_m_dataset_rank.csv")
    monthly1_df = pd.read_csv(DATA_DIR / "ridi_w2_dataset_rank.csv")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
    exit()

weekly_df = weekly1_df[weekly1_df["keywords"].str.contains("연재중", na=False)]
monthly_df = monthly1_df[monthly1_df["keywords"].str.contains("연재중", na=False)]

banned_words = [
    "평점",
    "별점",
    "리뷰",
    "개이상",
    "기다리면무료",
    "독점",
    "대여",
    "연재",
    "완결",
    "연재중",
    "단행본",
]


def get_clean_keywords(df_column):
    keywords = []
    for item in df_column:
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
                    keywords.append(clean_word)
    return Counter(keywords)


weekly_counts = get_clean_keywords(weekly_df["keywords"])
monthly_counts = get_clean_keywords(monthly_df["keywords"])

common_keywords = set(weekly_counts.keys()) & set(monthly_counts.keys())

data = []
for word in common_keywords:
    w_count = weekly_counts[word]
    m_count = monthly_counts[word]
    total = w_count + m_count

    data.append(
        {"Keyword": word, "Weekly": w_count, "Monthly": m_count, "Total": total}
    )

df_plot = pd.DataFrame(data).sort_values(by="Total", ascending=False).head(20)

plt.figure(figsize=(14, 10))
df_plot = df_plot.set_index("Keyword")

df_plot = df_plot.iloc[::-1]

ax = df_plot[["Monthly", "Weekly"]].plot(
    kind="barh", stacked=True, figsize=(12, 8), color=["#ffd700", "#ff6b6b"]
)

plt.title("주간 & 월간 베스트 중복 키워드 top20", fontsize=18)
plt.xlabel("등장 횟수(건)", fontsize=14)
plt.ylabel("키워드", fontsize=14)
plt.legend(["월간 베스트 누적", "주간 베스트 반영"], loc="lower right")
plt.grid(axis="x", linestyle="--", alpha=0.3)

for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy()

    if width > 5:
        ax.text(
            x + width / 2,
            y + height / 2,
            f"{int(width)}",
            ha="center",
            va="center",
            color="black",
            fontsize=9,
            fontweight="bold",
        )

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")

print(f"{SAVE_DIR} chart created")
