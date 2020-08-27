# 카카오 지도 데이터 수집하기
import urllib.request
import time
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from django.conf import settings
from . import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def add_data(local):
    driver = webdriver.Chrome("C://Program Files//chromedriver//chromedriver.exe")

    # 카카오 지도에 "XX 빵집" 검색
    driver.get(f"https://map.kakao.com/")

    search_box = driver.find_element_by_css_selector("#search\.keyword\.query")
    search_box.send_keys(f"{local} 빵집")
    search_box.send_keys(Keys.ENTER)

    time.sleep(3)

    links = driver.find_elements_by_css_selector("#info\.search\.place\.list > li")
    target = driver.find_element_by_css_selector("#info\.search\.place")
    banghae = driver.find_element_by_css_selector("#dimmedLayer")

    for link in links:
        try:
            a = link.find_element_by_css_selector(
                "div.info_item > div.contact.clickArea > a.moreview"
            )
            a.send_keys(Keys.ENTER)
            time.sleep(1)
            driver.switch_to_window(driver.window_handles[1])
            # 데이터생성 작업시작
            # name 정보수집
            name = driver.find_element_by_css_selector(
                "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2"
            )
            name_text = name.text

            # address 정보수집
            try:
                address = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(2) > div > span.txt_address"
                )
                address_text = address.text
            except:
                address_text = ""

            # phone_number 정보수집
            try:
                phone = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_contact > div > div > span > span.txt_contact"
                )
                phone_text = phone.text
            except:
                phone_text = ""

            try:
                # 영업일 더보기정보 클릭
                date_btn = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.location_present > ul > li > a"
                )
                date_btn.send_keys(Keys.ENTER)
                # business hour 정보수집
                business_hours = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.fold_floor > div > ul:nth-child(2)"
                )
                business_hours_text = business_hours.text
                # 뜬 창 닫기
                close_btn = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.fold_floor > div > a"
                )
                close_btn.send_keys(Keys.ENTER)
            except NoSuchElementException:
                try:
                    business_hours = driver.find_element_by_css_selector(
                        "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div > ul > li > span"
                    )
                    business_hours_text = business_hours.text
                except NoSuchElementException:
                    business_hours_text = ""

            # 스크롤 내리기
            body = driver.find_element_by_css_selector("body")
            body.send_keys(Keys.PAGE_DOWN)

            # sub_name 데이터 수집
            try:
                sub_name = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.open_on > div > p"
                )
                sub_name_text = sub_name.text
            except NoSuchElementException:
                sub_name_text = ""

            # menus_list 데이터 수집
            menus = driver.find_elements_by_css_selector("ul.list_menu > li")
            menus_list = []
            for menu in menus:
                if menu.find_element_by_css_selector("div span.loss_word").text == "":
                    break
                add = []
                add.append(menu.find_element_by_css_selector("div span.loss_word").text)
                try:
                    add.append(
                        int(
                            menu.find_element_by_css_selector(
                                "div em.price_menu"
                            ).text.replace(",", "")
                        )
                    )
                except:
                    pass
                menus_list.append(add)

            # 사진 데이터 수집
            try:
                photo_button = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a"
                )
                action = ActionChains(driver)
                action.move_to_element(photo_button).perform()
                photo_button.send_keys(Keys.ENTER)
                urls = []
                time.sleep(2)
                imgs = driver.find_elements_by_css_selector("ul.list_phtoview > li")
                for index, img in enumerate(imgs):
                    if index == 3:
                        break
                    link = img.find_element_by_css_selector("a")
                    link.send_keys(Keys.ENTER)
                    time.sleep(1)
                    real_link = driver.find_element_by_css_selector(
                        "#photoViewer > div.layer_body > div.view_photo > div.view_image > img"
                    )
                    urls.append(real_link.get_attribute("src"))
                time.sleep(3)
                chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
                random_names = []
                for name in range(len(urls)):
                    random_names.append(
                        "".join((random.choice(chars)) for x in range(10))
                    )
                for index, url in enumerate(urls):
                    # urlretrieve는 다운로드 함수
                    urllib.request.urlretrieve(
                        url,
                        os.path.join(
                            BASE_DIR,
                            f"uploads/bakery/bread_imgs/{random_names[index]}.jpg",
                        ),
                    )
            except:
                pass

            # lat,lng 정보수집
            driver.get(f"https://www.google.co.kr/maps/@37.053745,125.6553969,5z?hl=ko")

            google_search_box = driver.find_element_by_css_selector("#searchboxinput")
            google_search_box.send_keys(name_text)
            google_search_box.send_keys(Keys.ENTER)

            time.sleep(3)

            try:
                # 검색했는데 바로 상세로 안가고 목록으로 가면 가장 첫번째 목록 클릭
                go_to = driver.find_element_by_css_selector(
                    "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div:nth-child(1) > div.section-result-content > div.section-result-text-content"
                )
                go_to.send_keys(Keys.ENTER)

                time.sleep(3)

                lat_text = float(driver.current_url.split("@")[1].split(",")[0])
                lng_text = float(driver.current_url.split("@")[1].split(",")[1])

            except:
                # 목록이 안뜰경우
                try:
                    # 상세로 간 경우
                    ex = driver.find_element_by_css_selector(
                        "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div:nth-child(1) > h1 > span:nth-child(1)"
                    )
                    lat_text = float(driver.current_url.split("@")[1].split(",")[0])
                    lng_text = float(driver.current_url.split("@")[1].split(",")[1])
                except:
                    # 검색결과를 찾지 못한경우
                    lat_text = 0
                    lng_text = 0

            # print(
            #     name_text,
            #     sub_name_text,
            #     address_text,
            #     business_hours_text,
            #     lat_text,
            #     lng_text,
            #     phone_text,
            #     menus_list,
            # )
            try:
                bakery = models.Bakery.objects.get(name=name_text)
            except:
                models.Bakery.objects.create(
                    name=name_text,
                    sub_name=sub_name_text,
                    lat=lat_text,
                    lng=lng_text,
                    address=address_text,
                    phone_number=phone_text,
                    business_hour=business_hours_text,
                    city=local,
                )
                for index, url in enumerate(urls):
                    img = models.Photo()
                    img.bakery = models.Bakery.objects.get(name=name_text)
                    img.photo = f"bakery/bread_imgs/{random_names[index]}.jpg"
                    img.save()

                for index, menu in enumerate(menus_list):
                    m = models.Menu()
                    m.bakery = models.Bakery.objects.get(name=name_text)
                    m.name = menu[0]
                    try:
                        m.row_price = menu[1]
                    except:
                        pass
                    m.save()

            urls = []
            random_names = []
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        except NoSuchElementException:
            a.send_keys(Keys.PAGE_DOWN)
            links = driver.find_elements_by_css_selector(
                "#info\.search\.place\.list > li"
            )

    more = driver.find_element_by_css_selector("#info\.search\.place\.more")
    more.send_keys(Keys.ENTER)

    time.sleep(3)

    links = driver.find_elements_by_css_selector("#info\.search\.place\.list > li")

    for link in links:
        try:
            a = link.find_element_by_css_selector(
                "div.info_item > div.contact.clickArea > a.moreview"
            )
            a.send_keys(Keys.ENTER)
            time.sleep(1)
            driver.switch_to_window(driver.window_handles[1])
            # 데이터생성 작업시작
            # name 정보수집
            name = driver.find_element_by_css_selector(
                "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2"
            )
            name_text = name.text

            # address 정보수집
            try:
                address = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(2) > div > span.txt_address"
                )
                address_text = address.text
            except:
                address_text = ""

            # phone_number 정보수집
            try:
                phone = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_contact > div > div > span > span.txt_contact"
                )
                phone_text = phone.text
            except:
                phone_text = ""

            try:
                # 영업일 더보기정보 클릭
                date_btn = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.location_present > ul > li > a"
                )
                date_btn.send_keys(Keys.ENTER)
                # business hour 정보수집
                business_hours = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.fold_floor > div > ul:nth-child(2)"
                )
                business_hours_text = business_hours.text
                # 뜬 창 닫기
                close_btn = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.fold_floor > div > a"
                )
                close_btn.send_keys(Keys.ENTER)
            except NoSuchElementException:
                try:
                    business_hours = driver.find_element_by_css_selector(
                        "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div > ul > li > span"
                    )
                    business_hours_text = business_hours.text
                except NoSuchElementException:
                    business_hours_text = ""

            # 스크롤 내리기
            body = driver.find_element_by_css_selector("body")
            body.send_keys(Keys.PAGE_DOWN)

            # sub_name 데이터 수집
            try:
                sub_name = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.open_on > div > p"
                )
                sub_name_text = sub_name.text
            except NoSuchElementException:
                sub_name_text = ""

            # menus_list 데이터 수집
            menus = driver.find_elements_by_css_selector("ul.list_menu > li")
            menus_list = []
            for menu in menus:
                if menu.find_element_by_css_selector("div span.loss_word").text == "":
                    break
                add = []
                add.append(menu.find_element_by_css_selector("div span.loss_word").text)
                try:
                    add.append(
                        int(
                            menu.find_element_by_css_selector(
                                "div em.price_menu"
                            ).text.replace(",", "")
                        )
                    )
                except:
                    pass
                menus_list.append(add)

            # 사진 데이터 수집
            try:
                photo_button = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a"
                )
                action = ActionChains(driver)
                action.move_to_element(photo_button).perform()
                photo_button.send_keys(Keys.ENTER)
                urls = []
                time.sleep(2)
                imgs = driver.find_elements_by_css_selector("ul.list_phtoview > li")
                for index, img in enumerate(imgs):
                    if index == 3:
                        break
                    link = img.find_element_by_css_selector("a")
                    link.send_keys(Keys.ENTER)
                    time.sleep(1)
                    real_link = driver.find_element_by_css_selector(
                        "#photoViewer > div.layer_body > div.view_photo > div.view_image > img"
                    )
                    urls.append(real_link.get_attribute("src"))
                time.sleep(3)
                chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
                random_names = []
                for name in range(len(urls)):
                    random_names.append(
                        "".join((random.choice(chars)) for x in range(10))
                    )
                for index, url in enumerate(urls):
                    # urlretrieve는 다운로드 함수
                    urllib.request.urlretrieve(
                        url,
                        os.path.join(
                            BASE_DIR,
                            f"uploads/bakery/bread_imgs/{random_names[index]}.jpg",
                        ),
                    )
            except:
                pass

            # lat,lng 정보수집
            driver.get(f"https://www.google.co.kr/maps/@37.053745,125.6553969,5z?hl=ko")

            google_search_box = driver.find_element_by_css_selector("#searchboxinput")
            google_search_box.send_keys(name_text)
            google_search_box.send_keys(Keys.ENTER)

            time.sleep(3)

            try:
                # 검색했는데 바로 상세로 안가고 목록으로 가면 가장 첫번째 목록 클릭
                go_to = driver.find_element_by_css_selector(
                    "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div:nth-child(1) > div.section-result-content > div.section-result-text-content"
                )
                go_to.send_keys(Keys.ENTER)

                time.sleep(3)

                lat_text = float(driver.current_url.split("@")[1].split(",")[0])
                lng_text = float(driver.current_url.split("@")[1].split(",")[1])

            except:
                # 목록이 안뜰경우
                try:
                    # 상세로 간 경우
                    ex = driver.find_element_by_css_selector(
                        "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div:nth-child(1) > h1 > span:nth-child(1)"
                    )
                    lat_text = float(driver.current_url.split("@")[1].split(",")[0])
                    lng_text = float(driver.current_url.split("@")[1].split(",")[1])
                except:
                    # 검색결과를 찾지 못한경우
                    lat_text = 0
                    lng_text = 0

            # print(
            #     name_text,
            #     sub_name_text,
            #     address_text,
            #     business_hours_text,
            #     lat_text,
            #     lng_text,
            #     phone_text,
            #     menus_list,
            # )
            try:
                bakery = models.Bakery.objects.get(name=name_text)
            except:
                models.Bakery.objects.create(
                    name=name_text,
                    sub_name=sub_name_text,
                    lat=lat_text,
                    lng=lng_text,
                    address=address_text,
                    phone_number=phone_text,
                    business_hour=business_hours_text,
                    city=local,
                )
                for index, url in enumerate(urls):
                    img = models.Photo()
                    img.bakery = models.Bakery.objects.get(name=name_text)
                    img.photo = f"bakery/bread_imgs/{random_names[index]}.jpg"
                    img.save()

                for index, menu in enumerate(menus_list):
                    m = models.Menu()
                    m.bakery = models.Bakery.objects.get(name=name_text)
                    m.name = menu[0]
                    try:
                        m.row_price = menu[1]
                    except:
                        pass
                    m.save()

            urls = []
            random_names = []
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        except NoSuchElementException:
            a.send_keys(Keys.PAGE_DOWN)
            links = driver.find_elements_by_css_selector(
                "#info\.search\.place\.list > li"
            )
    # 2바퀴돌고 끝내기
    return

    page_3 = driver.find_element_by_css_selector("#info\.search\.page\.no3")
    page_3.send_keys(Keys.ENTER)

    time.sleep(3)

    links = driver.find_elements_by_css_selector("#info\.search\.place\.list > li")

    for link in links:
        try:
            a = link.find_element_by_css_selector(
                "div.info_item > div.contact.clickArea > a.moreview"
            )
            a.send_keys(Keys.ENTER)
            time.sleep(1)
            driver.switch_to_window(driver.window_handles[1])
            # 데이터생성 작업시작
            # name 정보수집
            name = driver.find_element_by_css_selector(
                "#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2"
            )
            name_text = name.text

            # address 정보수집
            try:
                address = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(2) > div > span.txt_address"
                )
                address_text = address.text
            except:
                address_text = ""

            # phone_number 정보수집
            try:
                phone = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.placeinfo_contact > div > div > span > span.txt_contact"
                )
                phone_text = phone.text
            except:
                phone_text = ""

            try:
                # 영업일 더보기정보 클릭
                date_btn = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.location_present > ul > li > a"
                )
                date_btn.send_keys(Keys.ENTER)
                # business hour 정보수집
                business_hours = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.fold_floor > div > ul:nth-child(2)"
                )
                business_hours_text = business_hours.text
                # 뜬 창 닫기
                close_btn = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div.fold_floor > div > a"
                )
                close_btn.send_keys(Keys.ENTER)
            except NoSuchElementException:
                try:
                    business_hours = driver.find_element_by_css_selector(
                        "#mArticle > div.cont_essential > div.details_placeinfo > div:nth-child(3) > div > div > ul > li > span"
                    )
                    business_hours_text = business_hours.text
                except NoSuchElementException:
                    business_hours_text = ""

            # 스크롤 내리기
            body = driver.find_element_by_css_selector("body")
            body.send_keys(Keys.PAGE_DOWN)

            # sub_name 데이터 수집
            try:
                sub_name = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_essential > div.details_placeinfo > div.placeinfo_default.open_on > div > p"
                )
                sub_name_text = sub_name.text
            except NoSuchElementException:
                sub_name_text = ""

            # menus_list 데이터 수집
            menus = driver.find_elements_by_css_selector("ul.list_menu > li")
            menus_list = []
            for menu in menus:
                if menu.find_element_by_css_selector("div span.loss_word").text == "":
                    break
                add = []
                add.append(menu.find_element_by_css_selector("div span.loss_word").text)
                try:
                    add.append(
                        int(
                            menu.find_element_by_css_selector(
                                "div em.price_menu"
                            ).text.replace(",", "")
                        )
                    )
                except:
                    pass
                menus_list.append(add)

            # 사진 데이터 수집
            try:
                photo_button = driver.find_element_by_css_selector(
                    "#mArticle > div.cont_photo > div.photo_area > ul > li.size_l > a"
                )
                action = ActionChains(driver)
                action.move_to_element(photo_button).perform()
                photo_button.send_keys(Keys.ENTER)
                urls = []
                time.sleep(2)
                imgs = driver.find_elements_by_css_selector("ul.list_phtoview > li")
                for index, img in enumerate(imgs):
                    if index == 3:
                        break
                    link = img.find_element_by_css_selector("a")
                    link.send_keys(Keys.ENTER)
                    time.sleep(1)
                    real_link = driver.find_element_by_css_selector(
                        "#photoViewer > div.layer_body > div.view_photo > div.view_image > img"
                    )
                    urls.append(real_link.get_attribute("src"))
                time.sleep(3)
                chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
                random_names = []
                for name in range(len(urls)):
                    random_names.append(
                        "".join((random.choice(chars)) for x in range(10))
                    )
                for index, url in enumerate(urls):
                    # urlretrieve는 다운로드 함수
                    urllib.request.urlretrieve(
                        url,
                        os.path.join(
                            BASE_DIR,
                            f"uploads/bakery/bread_imgs/{random_names[index]}.jpg",
                        ),
                    )
            except:
                pass

            # lat,lng 정보수집
            driver.get(f"https://www.google.co.kr/maps/@37.053745,125.6553969,5z?hl=ko")

            google_search_box = driver.find_element_by_css_selector("#searchboxinput")
            google_search_box.send_keys(name_text)
            google_search_box.send_keys(Keys.ENTER)

            time.sleep(3)

            try:
                # 검색했는데 바로 상세로 안가고 목록으로 가면 가장 첫번째 목록 클릭
                go_to = driver.find_element_by_css_selector(
                    "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div:nth-child(1) > div.section-result-content > div.section-result-text-content"
                )
                go_to.send_keys(Keys.ENTER)

                time.sleep(3)

                lat_text = float(driver.current_url.split("@")[1].split(",")[0])
                lng_text = float(driver.current_url.split("@")[1].split(",")[1])

            except:
                # 목록이 안뜰경우
                try:
                    # 상세로 간 경우
                    ex = driver.find_element_by_css_selector(
                        "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header-title > div.section-hero-header-title-top-container > div.section-hero-header-title-description > div:nth-child(1) > h1 > span:nth-child(1)"
                    )
                    lat_text = float(driver.current_url.split("@")[1].split(",")[0])
                    lng_text = float(driver.current_url.split("@")[1].split(",")[1])
                except:
                    # 검색결과를 찾지 못한경우
                    lat_text = 0
                    lng_text = 0

            # print(
            #     name_text,
            #     sub_name_text,
            #     address_text,
            #     business_hours_text,
            #     lat_text,
            #     lng_text,
            #     phone_text,
            #     menus_list,
            # )
            try:
                bakery = models.Bakery.objects.get(name=name_text)
            except:
                models.Bakery.objects.create(
                    name=name_text,
                    sub_name=sub_name_text,
                    lat=lat_text,
                    lng=lng_text,
                    address=address_text,
                    phone_number=phone_text,
                    business_hour=business_hours_text,
                    city=local,
                )
                for index, url in enumerate(urls):
                    img = models.Photo()
                    img.bakery = models.Bakery.objects.get(name=name_text)
                    img.photo = f"bakery/bread_imgs/{random_names[index]}.jpg"
                    img.save()

                for index, menu in enumerate(menus_list):
                    m = models.Menu()
                    m.bakery = models.Bakery.objects.get(name=name_text)
                    m.name = menu[0]
                    try:
                        m.row_price = menu[1]
                    except:
                        pass
                    m.save()

            urls = []
            random_names = []
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        except NoSuchElementException:
            a.send_keys(Keys.PAGE_DOWN)
            links = driver.find_elements_by_css_selector(
                "#info\.search\.place\.list > li"
            )

