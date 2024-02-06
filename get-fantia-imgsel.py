import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
import pickle
from time import sleep
import urllib
import os

# postname input
print('投稿IDを入力（postのURLの末尾の番号）')
post_id = input('input number: ')
print(f'your input: {post_id}')

path_check = "/volumes/your_dir"
print(os.path.isdir(path_check))

if not os.path.isdir(path_check):
    print("ディレクトリにアクセスできていないかも")
    exit()

driver = webdriver.Chrome()

login_data = {
   'user[email]': '',
   'user[password]': ''
}
cookies_file = 'cookie.pkl'

url = 'https://fantia.jp/sessions/signin'
driver.get(url)

# ログイン
name_box = driver.find_element(By.NAME,'user[email]')
name_box.send_keys(login_data['user[email]'])
password_box = driver.find_element(By.NAME,'user[password]')
password_box.send_keys(login_data['user[password]'])
remember_box = driver.find_element(By.CSS_SELECTOR,("form#new_user .btn"))
remember_box.click()

cookies = driver.get_cookies() # クッキーを取得する
pickle.dump(cookies,open(cookies_file,'wb')) # クッキーを保存する

sleep(30)

driver.get("https://fantia.jp/posts/" + post_id)

sleep(3)

def downloader( driver ):
    elem_img = driver.find_elements(By.CLASS_NAME,("image-container"))
    for index, i in enumerate(elem_img):
        img_list = driver.find_elements(By.CLASS_NAME,("image-container"))
        elem_h1 = driver.find_elements(By.TAG_NAME, "h1")
        h1_text = elem_h1[1].text
        filename_count = str(index+1) + '-' + str(len(elem_img))
        img_list[index].click()
        btn = driver.find_elements(By.CSS_SELECTOR,("a.btn.btn-secondary"))
        btn[0].click()
        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        img = driver.find_element(By.TAG_NAME, ("img"))
        img_url = img.get_attribute("src")
        with urllib.request.urlopen(img_url)as rf:
            img_data = rf.read()
        path = path_check
        print(path+str(h1_text)+"-"+filename_count+".png")
        with open(path+str(h1_text)+"-"+filename_count+".png", mode="wb")as wf:
            wf.write(img_data)
        driver.close()
        driver.switch_to.window(original_window)

        btn = driver.find_elements(By.CSS_SELECTOR,("a.btn.btn-dark"))
        btn[0].click()

while True:
    downloader( driver )
    next = driver.find_elements(By.CLASS_NAME,("post-next"))
    if next:
        next[1].click()
        sleep(5)
    else:
        break
