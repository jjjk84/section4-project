from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import csv
from selenium.webdriver.common.action_chains import ActionChains

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
service = Service(executable_path='/Users/jjjk84/Downloads/chromedriver_mac_arm64')
driver = webdriver.Chrome(service=service, options=chrome_options)

def crawl():
    driver.get("https://www.vivino.com/explore?e=eJzLLbI11rNQy83MszVQy02ssDU1AAG15Epb7yC1ZCARrlZga6iWnmZblliUmVqSmKOWX5Rim5JanKyWn1RpW5RYkpmXXhyfWJZalJieCgDgwxqj")
    driver.implicitly_wait(10) # 로딩이 끝날 때까지 10초까지는 기다려줌
    
    f = open(r"/Users/jjjk84/Documents/Section4/project/data4.csv", 'w', newline="")
    writer = csv.writer(f)
    cnt=0
    # 상품 정보 div(list 형태로 반환)
    types_div = driver.find_element(By.CSS_SELECTOR, ".filterByWineType__items--2GBgf")
    types = types_div.find_elements(By.CSS_SELECTOR, ".pill__inner--2uty5")[0]
    
    
    for type in types:
        type.click()
        time.sleep(10)

        before_h = driver.execute_script("return window.scrollY")
        
        while True:
            # 맨 아래로 스크롤 내리기
            # driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 500)")
            # 스크롤 사이 페이지 로딩 시간
            time.sleep(5)

            # 스크롤 후 높이
            after_h = driver.execute_script("return window.scrollY")

            
            if after_h == before_h:
                break
            before_h = after_h

        items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="wineCard"]')
        print(len(items))

        while True:
            
            for item in items:
                # ActionChains(driver).move_to_element(temp[i]).perform()   
                time.sleep(3)
                
                try:
                    try:
                        ActionChains(driver).key_down(Keys.COMMAND).click(item).key_up(Keys.COMMAND).perform()
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(5)
                        
                        url = driver.current_url
                        # price = driver.find_element(By.CSS_SELECTOR, ".purchaseAvailabilityPPC__amount--2_4GT").text
                        
                        # name_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[5]/div/div/div[2]/div[1]/div/h1/span[2]")))
                        # name = name_element.text
                        
                        # score = driver.find_element(By.CSS_SELECTOR, ".vivinoRating_averageValue__uDdPM").text
                        
                        # driver.execute_script("window.scrollBy(0, window.innerHeight);")

                        # lst_ele = driver.find_elements(By.CSS_SELECTOR, ".indicatorBar__progress--3aXLX")

                        # ele_temp=[]
                        # for ele in lst_ele:
                        #     ele_temp.append(ele.get_attribute('style'))
                        
                        # data = [name, price, score, ele_temp, url]

                        data = url
                        writer.writerow(data)
                        cnt+=1
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                    except IndexError:
                        cnt+=1
                        continue

                except StaleElementReferenceException:
                    items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="wineCard"]')[840:]
                    item = items[cnt]
                    
                    try:
                        ActionChains(driver).key_down(Keys.COMMAND).click(item).key_up(Keys.COMMAND).perform()
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(5)
                        
                        url = driver.current_url
                        # price = driver.find_element(By.CSS_SELECTOR, ".purchaseAvailabilityPPC__amount--2_4GT").text
                        
                        # name_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[5]/div/div/div[2]/div[1]/div/h1/span[2]")))
                        # name = name_element.text
                        
                        
                        # score = driver.find_element(By.CSS_SELECTOR, ".vivinoRating_averageValue__uDdPM").text
                        
                        
                        # driver.execute_script("window.scrollBy(0, window.innerHeight);")
                        # time.sleep(5)
                        # lst_ele = driver.find_elements(By.CSS_SELECTOR, ".indicatorBar__progress--3aXLX")
                        # ele_temp=[]
                        # for ele in lst_ele:
                        #     ele_temp.append(ele.get_attribute('style'))
                        
                        # data = [name, price, score, ele_temp]
                        data = url
                        writer.writerow(data)
                        cnt+=1

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    
                    except IndexError:
                        cnt+=1
                        continue

            # 스크롤이 끝까지 도달했는지 확인합니다.
            if cnt == len(items):
                break
        
        type.click()
        time.sleep(5)
    
    f.close()
        
        # SCROLL_PAUSE_TIME = 2

        # items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="wineCard"]')
        # temp = [item for item in items]
        

        # while True:
        #     for item in temp:
        #         try:
        #             ActionChains(driver).move_to_element(item).perform()
        #             item.click()
        #             WebDriverWait(driver, 10).until(EC.staleness_of(item))
                    
        #             driver.back()
        #         except StaleElementReferenceException:
        #             print("StaleElementReferenceException occurred")
        #     # 스크롤을 내리기 위해 JavaScript 코드를 실행합니다.
        #     # 'window.scrollBy(0, window.innerHeight);' 코드는 현재 뷰포트(화면)의 높이만큼 스크롤을 내립니다.
        #     # 'window.scrollBy(0, document.body.scrollHeight);' 코드는 페이지 전체 높이만큼 스크롤을 내립니다.
        #     driver.execute_script("window.scrollBy(0, window.innerHeight);")
        #     time.sleep(SCROLL_PAUSE_TIME)
            
        #     # 다음 스크롤에서 새로운 요소를 찾기 위해 리스트를 업데이트합니다.
        #     items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="wineCard"]')
        #     temp = [item for item in items if item not in temp]
            
        #     # 스크롤이 끝까지 도달했는지 확인합니다.
        #     last_height = driver.execute_script("return document.body.scrollHeight")
        #     new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        #     if new_height >= last_height:
        #         break

        
        # # 쇼핑 메뉴 클릭, 이동
        # shopping = driver.find_element(By.CSS_SELECTOR,"#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix > li:nth-child(5) > a")
        # shopping.click()
        # time.sleep(2)

        # # 검색창 클릭
        # search = driver.find_element(By.CSS_SELECTOR, "#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div._searchInput_search_input_QXUFf > input")
        # search.click()

        # # 검색어 입력
        # search.send_keys("아이폰 13")
        # search.send_keys(Keys.ENTER)

        # # 무한 스크롤

        # # 스크롤 전 높이
        # before_h = driver.execute_script("return window.scrollY")

        # while True:
        #     # 맨 아래로 스크롤 내리기
        #     driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

        #     # 스크롤 사이 페이지 로딩 시간
        #     time.sleep(1)

        #     # 스크롤 후 높이
        #     after_h = driver.execute_script("return window.scrollY")

        #     if after_h == before_h:
        #         break
        #     before_h = after_h

        # # 상품 정보 div
        # items = driver.find_elements(By.CSS_SELECTOR, ".basicList_info_area__TWvzp")

        # for item in items:
        #     name = item.find_element(By.CSS_SELECTOR, ".basicList_link__JLQJf").text
        #     price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
        #     link = item.find_element(By.CSS_SELECTOR, ".basicList_link__JLQJf").get_attribute('href')
        #     print(name, price, link)

        # 마지막 타입 클릭 해제

crawl()
