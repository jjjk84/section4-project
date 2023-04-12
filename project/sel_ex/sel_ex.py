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

# 브라우저 생성
browser=webdriver.Chrome("User/jjjk84/Documents/chromedriver")

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://www.naver.com")
browser.implicitly_wait(3) # 로딩이 끝날 때까지 10초까지는 기다려줌

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
