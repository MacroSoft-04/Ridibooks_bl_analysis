from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import csv
import random


def init_driver():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument(
        "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": """
            Object.defineProperty(navigator, 'webdriver',{
            get: ()=> undifined
            })
        """},
    )
    return driver


def do_login(driver):
    print("=" * 50)
    print("브라우저에서 직접 로그인을 진행해주세요")
    print("터미널에서 엔터키 입력 시 수집 시작")

    driver.get(
        "https://ridibooks.com/account/login?state=%7B%22return_url%22%3A%22https%3A%2F%2Fridibooks.com%2Fbl%2Fwebnovel%22%7D"
    )

    input()

    print("확인 완료! 데이터 수집 시작")


if __name__ == "__main__":
    links = []
    with open("ridi_m_bl_links.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            links.append(row[0])

    print(f"총 {len(links)}개 생성")

    driver = init_driver()
    do_login(driver)

    with open("ridi_dataset_final.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "author", "keywords", "link"])

        for i, link in enumerate(links):
            try:
                print(f"[{i+1}/{len(links)}] 접속 중...{link}")
                driver.get(link)
                time.sleep(random.uniform(2, 3))
                soup = BeautifulSoup(driver.page_source, "html.parser")

                title_tag = soup.select_one("h1")
                title = title_tag.text.strip() if title_tag else "제목 못 찾음"

                author = "작가 못 찾음"
                list_items = soup.select("li")
                for item in list_items:
                    if "저자" in item.text:
                        author = item.text.replace("저자", "").strip()
                        break

                keywords_tags = soup.select("button[aria-label]")
                keywords = [tag["aria-label"] for tag in keywords_tags]
                keywords_str = ", ".join(keywords)

                # 결과 출력
                print(f"제목 : {title}")
                print(f"작가: {author}")
                print(f"키워드 : {keywords}")

                writer.writerow([title, author, keywords_str, link])
                print(f"완료! ({title})")

                if (i + 1) % 10 == 0:
                    print("get {i + 1}. take break for a while")
                    time.sleep(2)

            except Exception as e:
                print(f"error ({link}): {e}")
                continue

driver.quit()
print("test done")
