import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from collections import Counter
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[2]
BASE_DIR = SRC_DIR.parent
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SAVE_DIR = OUTPUT_DIR / "trend_genres_themes.jpg"

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

# load data & set up except target
try:
    # 카테고리 기준표
    keyword_map = pd.read_csv(DATA_DIR / "ridi_keyword.csv")
    keyword_map["카테고리"] = keyword_map["카테고리"].str.strip()
    keyword_map["키워드"] = keyword_map["키워드"].str.strip()

    # 랭킹 데이터
    weekly_original = pd.read_csv(DATA_DIR / "ridi_w2_dataset_rank.csv")
    monthly_original = pd.read_csv(DATA_DIR / "ridi_m_dataset_rank.csv")

    # 노이즈 제거
    weekly_df = weekly_original[
        weekly_original["keywords"].str.contains("연재중", na=False)
    ]
    monthly_df = monthly_original[
        monthly_original["keywords"].str.contains("연재중", na=False)
    ]

except FileNotFoundError:
    print("there isn't any file")
    exit()

# reject keyword
character_keywords = set(
    keyword_map[keyword_map["카테고리"].isin(["인물(공)", "인물(수)"])]["키워드"]
)

noise_words = [
    "연재중",
    "완결",
    "평점",
    "리뷰",
    "개이상",
    "단행본",
    "기다리면무료",
    "독점",
    "대여",
    "소장",
    "별점",
    "19세",
    "고수위",
    "BL",
    "웹소설",
]
character_keywords.update(noise_words)


# keyword sort criteria (genre vs mood)
genre_keywords = [
    "현대물",
    "판타지물",
    "오메가버스",
    "가이드버스",
    "동양풍",
    "서양풍",
    "시대물",
    "학원/캠퍼스물",
    "차원이동/영혼바뀜",
    "연예계",
    "정치/사회/재벌",
    "리맨물",
    "스포츠",
    "SF/미래물",
    "게임물",
    "사극",
    "궁정물",
]
# last will become "mood/소재"


# ---------------------------------------------------------
# 🛠️ 3. 데이터 가공 함수
# ---------------------------------------------------------
def get_clean_counts(df_column):
    keywords = []
    for item in df_column:
        if isinstance(item, str):
            words = item.split(",")
            for w in words:
                clean_w = w.strip()
                if not clean_w:
                    continue
                if clean_w in character_keywords:
                    continue
                is_noise = False
                for noise in noise_words:
                    if (
                        noise in clean_w
                    ):  # 예: '평점'이 '평점4점이상' 안에 있는가? -> True
                        is_noise = True
                        break
                if is_noise:
                    continue
                keywords.append(clean_w)
    return Counter(keywords)


w_counts = get_clean_counts(weekly_df["keywords"])
m_counts = get_clean_counts(monthly_df["keywords"])

all_keys = set(w_counts.keys()) | set(m_counts.keys())
data = []

for k in all_keys:
    w = w_counts[k]
    m = m_counts[k]
    total = w + m

    # 색상 결정
    if any(g in k for g in genre_keywords):
        color = "#a55eea"  # 🟣 보라색 (장르/배경)
    else:
        color = "#e67e22"  # 🟠 주황색 (사건/소재/분위기)

    data.append(
        {"Keyword": k, "Weekly": w, "Monthly": m, "Total": total, "Color": color}
    )

# Top 20 추출 및 정렬
df_top = pd.DataFrame(data).sort_values(by="Total", ascending=False).head(20)
df_top = df_top.iloc[::-1]

# ---------------------------------------------------------
# 📊 4. 시각화 (단독 그래프)
# ---------------------------------------------------------
plt.figure(figsize=(12, 12))

y_pos = range(len(df_top))

# 1. 월간 데이터 (베이스)
bars_base = plt.barh(
    y_pos, df_top["Monthly"], color="#2d3436", label="월간 누적", height=0.6
)

# 2. 주간 데이터 (트렌드)
bars_trend = plt.barh(
    y_pos, df_top["Weekly"], left=df_top["Monthly"], color=df_top["Color"], height=0.6
)

# 3. 숫자 내부 표시 (White Bold)
for p in bars_base:
    width = p.get_width()
    if width > 3:
        plt.text(
            p.get_x() + width / 2,
            p.get_y() + p.get_height() / 2,
            f"{int(width)}",
            ha="center",
            va="center",
            color="white",
            fontsize=10,
            fontweight="bold",
        )

for p in bars_trend:
    width = p.get_width()
    if width > 3:
        plt.text(
            p.get_x() + width / 2,
            p.get_y() + p.get_height() / 2,
            f"{int(width)}",
            ha="center",
            va="center",
            color="white",
            fontsize=10,
            fontweight="bold",
        )

# 축 및 라벨 설정
plt.yticks(y_pos, df_top["Keyword"], fontsize=13, fontweight="bold")
plt.title(
    "🌍 장르(세계관) & 소재(사건) 핵심 트렌드 Top 20",
    fontsize=20,
    fontweight="bold",
    pad=20,
)
plt.xlabel("등장 횟수 (건)", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.3)

# 범례
legend_elements = [
    Line2D([0], [0], color="#2d3436", lw=8, label="⬛ 월간 베이스 (검증된 인기)"),
    Line2D([0], [0], color="white", lw=0, label="  "),
    Line2D([0], [0], color="#a55eea", lw=8, label="🟪 주간 트렌드: 장르/세계관 (배경)"),
    Line2D(
        [0], [0], color="#e67e22", lw=8, label="🟧 주간 트렌드: 소재/사건 (Key Point)"
    ),
]

plt.legend(
    handles=legend_elements,
    loc="lower right",
    fontsize=12,
    frameon=True,
    facecolor="white",
    edgecolor="black",
)

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")

print(f"{SAVE_DIR} chart complete")
