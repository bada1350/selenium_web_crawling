from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
import os

url_list = []
folder_name = []
URL_HEAD = "https://www.onekitprojects.com/51515/"

# 크롬 드라이버 자동 업데이트
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.onekitprojects.com/51515")

# 페이지 로드 대기
time.sleep(3)

SCROLL_PAUSE_TIME = 2

# 스크롤 높이 가져오기
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 아래로 끝까지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로드 대기
    time.sleep(SCROLL_PAUSE_TIME)

    # 새 스크롤 높이 계산 및 기존의 스크롤 높이와 비교
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".StylableButton2545352419__root.style-l1b4sq3m3__root").click()
            time.sleep(2)
        except:
            break
    last_height = new_height

title = driver.find_elements(By.CSS_SELECTOR, ".info-member.info-element-title")

for t in title:
    target = t.text
    url_list.append(target)
    folder_name.append(target)

for i, url in enumerate(url_list):
    url = URL_HEAD + url.replace(" ", "-").lower()
    url_list[i] = url

print(url_list)

# 현재 위치에 '자료 모음' 폴더 생성
os.mkdir("./자료 모음")

# '자료 모음' 폴더 내부에 프로젝트 자료들을 저장할 폴더 생성
for n in folder_name:
    os.mkdir("./자료 모음/{}".format(n))

for i, url in enumerate(url_list):
    res = requests.get(url)
    if res.status_code == 200:
        html = res.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # Image 자료 저장
        target_img = soup.select("img.gallery-item-visible.gallery-item.gallery-item-preloaded")

        for idx, img in enumerate(target_img):
            try:
                ImgUrl = img["src"]
                img_res = requests.get(ImgUrl)
                img_data = img_res.content
                file = open("./자료 모음/{}/{}.jpg".format(folder_name[i], folder_name[i] + str(idx + 1)), "wb")
                file.write(img_data)
                file.close()
            except:
                pass
        
        # Building Instructions(PDF 파일) 저장
        target_pdf = soup.select("a.AyFEbi")
        pdf_name = soup.select(".Zc7IjY p.font_8")

        for p, n in zip(target_pdf, pdf_name):
            try:
                PDF_Url = p["href"]
                PDF_Name = n.string
                pdf_res = requests.get(PDF_Url)
                pdf_data = pdf_res.content
                file = open("./자료 모음/{}/{}.pdf".format(folder_name[i], PDF_Name), "wb")
                file.write(pdf_data)
                file.close()
            except:
                pass
        
        # Programming 자료 저장
        programing_download_url = soup.select_one(".StylableButton2545352419__root.style-l17yovyx1__root.StylableButton2545352419__link")["href"]
        urllib.request.urlretrieve(programing_download_url, "./자료 모음/{}/{} Programming.zip".format(folder_name[i], folder_name[i]))
    else:
        pass