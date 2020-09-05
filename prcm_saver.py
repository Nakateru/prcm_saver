"""
for
https://prcm.jp/

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, re, wget


def makefolder(path):
    path = re.sub(r'[\\/:*?"<>|]', '', path)
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print('Created folder ' + path + ' successfully')
        else:
            print('Folder existed')
    except Exception:
        print('Creating Folder Failed')
        driver.quit()
        exit()


def get_pic():
    items = driver.find_element_by_id('imglist_container').find_elements_by_tag_name('a')

    for i in items:
        item = i.find_element_by_tag_name('img').get_attribute('src')
        # print(item)
        match = re.search(r"https://pics.prcm.jp/(.+)/(.+)/(.+)/(.+)", item)
        img_url = 'https://pics.prcm.jp/' + match.group(1) + '/' + match.group(2) + '/' + match.group(
            3) + '/' + match.group(2) + '.' + match.group(3)
        img_list.append(img_url)
    print(len(img_list), 'images Found')
    # print(img_list)


def save_pic(url, path):
    try:
        name = re.split("/", url)[-1]
        filename = wget.download(url, path + '/' + name)
        print('Saved', filename)
    except:
        print(url)


def exist_next_page():
    flag = True
    try:
        driver.find_element_by_xpath("//div[@class='page-navigation']//li[@class='page-navigation__next']")
        return flag
    except:
        flag = False
        return flag


if __name__ == '__main__':
    print('prcm saver')
    print('Author  :  Nakateru (2020.09.05)')
    img_list = []

    Firsturl = "https://prcm.jp/list/%E6%B1%9F%E7%B1%A0%E8%A3%95%E5%A5%88?page=1"

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(Firsturl)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "imglist_container")))

    get_pic()

    while True:
        get_pic()
        driver.find_element_by_xpath("//div[@class='page-navigation']//li[@class='page-navigation__next']").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='page-navigation']//li[@class='page-navigation__prev']")))
        url = driver.current_url
        # print(url)
        num = re.split("page=", url)[-1]
        print('Turned to page', num)
        if exist_next_page():
            pass
            # if num == '102':
            #     break
            # else:
            #     pass
        else:
            break

    path = 'ego'
    makefolder(path)
    for i in img_list:
        save_pic(i, path)

    print('Done')
    driver.quit()
