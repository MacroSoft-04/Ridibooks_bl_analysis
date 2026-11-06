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
SAVE_DIR = OUTPUT_DIR / "keyword_trend.png"

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

try:
    weeky_original = pd.read_csv(DATA_DIR / "ridi_w2_dataset_rank.csv")
    monthly_original = pd.read_csv(DATA_DIR / "ridi_m_dataset_rank.csv")
except FileNotFoundError:
    print("There is no file")
    exit()

weekly_df = weeky_original[weeky_original["keywords"].str.contains("연재중", na=False)]
monthly_df = monthly_original[
    monthly_original["keywords"].str.contains("연재중", na=False)
]

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


w_counts = get_clean_keywords(weekly_df["keywords"])
m_counts = get_clean_keywords(monthly_df["keywords"])

common_keywords = set(w_counts.keys()) & set(m_counts.keys())

data = []
for word in common_keywords:
    w = w_counts[word]
    m = m_counts[word]

    diff = w - m
    total = w + m

    data.append(
        {"Keyword": word, "Weekly": w, "Monthly": m, "Diff": diff, "Total": total}
    )

df_trend = pd.DataFrame(data).sort_values(by="Total", ascending=False).head(30)
df_trend = df_trend.sort_values(by="Diff", ascending=True)

plt.figure(figsize=(14, 12))

colors = ["#ff6b6b" if x >= 0 else "#4dabf7" for x in df_trend["Diff"]]

plt.hlines(
    y=df_trend["Keyword"],
    xmin=0,
    xmax=df_trend["Diff"],
    color=colors,
    alpha=0.6,
    linewidth=5,
)
plt.scatter(df_trend["Diff"], df_trend["Keyword"], color=colors, s=100, alpha=1)

plt.axvline(x=0, color="gray", linestyle="--", linewidth=1)

plt.title("키워드 트렌드 온도계: 급상승(Hot) vs 안정권(Cool)", fontsize=18)
plt.xlabel("< 월간 우세(스테디셀러) | 주간우세(급상승 트렌드) >", fontsize=12)

for i, (diff, w, m) in enumerate(
    zip(df_trend["Diff"], df_trend["Weekly"], df_trend["Monthly"])
):
    offset = 0.5 if diff >= 0 else -0.5
    ha_pos = "left" if diff >= 0 else "right"
    plt.text(
        diff + offset,
        i,
        f"{diff:+}(주{w}/월{m})",
        va="center",
        ha=ha_pos,
        fontsize=9,
        color="black",
    )

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")

print(f"{SAVE_DIR} chart created")
