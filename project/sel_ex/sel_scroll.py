from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://www.naver.com")
driver.implicitly_wait(3) # 로딩이 끝날 때까지 10초까지는 기다려줌

# 쇼핑 메뉴 클릭, 이동
shopping = driver.find_element(By.CSS_SELECTOR,"#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix > li:nth-child(5) > a")
shopping.click()
time.sleep(2)

# 검색창 클릭
search = driver.find_element(By.CSS_SELECTOR, "#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div._searchInput_search_input_QXUFf > input")
search.click()

# 검색어 입력
search.send_keys("아이폰 13")
search.send_keys(Keys.ENTER)

# 무한 스크롤

# 스크롤 전 높이
before_h = driver.execute_script("return window.scrollY")

while True:
    # 맨 아래로 스크롤 내리기
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1)

    # 스크롤 후 높이
    after_h = driver.execute_script("return window.scrollY")

    if after_h == before_h:
        break
    before_h = after_h

# 상품 정보 div
items = driver.find_elements(By.CSS_SELECTOR, ".basicList_info_area__TWvzp")

for item in items:
    name = item.find_element(By.CSS_SELECTOR, ".basicList_link__JLQJf").text
    price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
    link = item.find_element(By.CSS_SELECTOR, ".basicList_link__JLQJf").get_attribute('href')
    print(name, price, link)
