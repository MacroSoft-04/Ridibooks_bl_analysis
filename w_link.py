from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_book_links(html, base_url):
    soup = BeautifulSoup(html,"html.parser")
    links = soup.select("a[href]")
    result = []

    for a in links:
        href = a.attrs['href']

        if '/books/'in href and 'rdt_idx' in href and 'pdf' not in href:
            url = urljoin(base_url, href)
            if url not in result:
                result.append(url)

    return result

all_book_links = []

for page_num in range(1, 5):
    print(f"현재 {page_num}페이지 접속중...", end=" ")

    target_url = f'https://ridibooks.com/bestsellers/bl-webnovel?page={page_num}&order=monthly'
    driver.get(target_url)
    time.sleep(2)
    last_scroll = driver.execute_script("return window.pageYOffset")

    while True:
        driver.execute_script("window.scrollTo(0, window.pageYOffset + 500);")
        time.sleep(2)
        new_scroll=driver.execute_script("return window.pageYOffset")
        
        if new_scroll == last_scroll:
            break
        last_scroll = new_scroll

    html = driver.page_source
    links = get_book_links(html, target_url)
    all_book_links.extend(links)

    print(f"완료! (발견된 책{len(links)}개)")

driver.quit()

all_book_links = list(set(all_book_links))

print("="*30)
print(f"최종 수집된 책 개수: {len(all_book_links)}개")

save_filename = 'ridi_w2_bl_links.csv'

with open(save_filename,'w', encoding='utf-8-sig',newline='')as f:
    writer = csv.writer(f)
    writer.writerow(['link'])
    for url in all_book_links:
        writer.writerow([url])

print(f"'{save_filename}'파일로 안전하게 저장했습니다!")
