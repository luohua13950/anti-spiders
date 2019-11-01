__author__ = 'luohua139'
import re
import time
import os
from PIL import Image
from urllib import parse
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

web = webdriver.Chrome(executable_path="..\\data\\webdriver\\chromedriver.exe")
wait = WebDriverWait(web,timeout=15)
base = "..\\data\\bilibili\\"
def login():
    web.maximize_window()
    url = "https://passport.bilibili.com/login"
    username = "abcd"
    passwd = "123456"
    web.get(url)
    user = wait.until(EC.presence_of_element_located((By.ID,"login-username")))
    password = wait.until(EC.presence_of_element_located((By.ID,"login-passwd")))

    user.send_keys(username)
    password.send_keys(passwd)

    logn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"a.btn.btn-login")))
    time.sleep(2)
    logn.click()
    time.sleep(6)
    dst_pic()
    web.close()



def hide_element(element):
    web.execute_script("arguments[0].style=arguments[1]",element,"display: none;")

def show_element(element):
    web.execute_script("arguments[0].style=arguments[1]",element,"display: block;")

def save_pic(element,name):
    web.save_screenshot("..\\data\\bilibili\\bilibili.png")
    left = element.location["x"]
    top = element.location["y"]
    right = left+element.size["width"]
    bottom = top+element.size["height"]
    print(left,top)
    print(right,bottom)
    im = Image.open("..\\data\\bilibili\\bilibili.png")
    im = im.crop((left,top,right,bottom))
    filename = os.path.join(base,name+".png")
    im.save(filename)

def dst_pic():
    full_pic_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute")))
    slice_pic_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"canvas.geetest_canvas_slice.geetest_absolute")))
    bg_pic_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"canvas.geetest_canvas_bg.geetest_absolute")))
    print("隐藏滑块")
    hide_element(slice_pic_element)
    save_pic(bg_pic_element,"bg")
    print("展示滑块")
    show_element(slice_pic_element)
    save_pic(slice_pic_element,"slice")
    print("展示原图")
    show_element(full_pic_element)
    save_pic(full_pic_element,"full")

if __name__ == "__main__":
    login()
    ActionChains(web).move_by_offset()