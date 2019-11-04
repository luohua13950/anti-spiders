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
wait = WebDriverWait(web, timeout=15)
base = "..\\data\\bilibili\\"


def login():
    web.maximize_window()
    url = "https://passport.bilibili.com/login"
    username = "15901889707"
    passwd = "xiangcao2717"
    web.get(url)
    user = wait.until(EC.presence_of_element_located((By.ID, "login-username")))
    password = wait.until(EC.presence_of_element_located((By.ID, "login-passwd")))

    user.send_keys(username)
    password.send_keys(passwd)

    logn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-login")))
    time.sleep(2)
    logn.click()
    time.sleep(6)
    dst_pic()


def hide_element(element):
    web.execute_script("arguments[0].style=arguments[1]", element, "display: none;")


def show_element(element):
    web.execute_script("arguments[0].style=arguments[1]", element, "display: block;")


def save_pic(element, name):
    web.save_screenshot("..\\data\\bilibili\\bilibili.png")
    left = element.location["x"]
    top = element.location["y"]
    right = left + element.size["width"]
    bottom = top + element.size["height"]
    im = Image.open("..\\data\\bilibili\\bilibili.png")
    im = im.crop((left, top, right, bottom))
    filename = os.path.join(base, name + ".png")
    im.save(filename)


def dst_pic():
    full_pic_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute")))
    slice_pic_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_slice.geetest_absolute")))
    bg_pic_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_bg.geetest_absolute")))
    hide_element(slice_pic_element)
    save_pic(bg_pic_element, "bg")
    print("保存背景图片")
    show_element(slice_pic_element)
    save_pic(slice_pic_element, "slice")
    print("保存带滑块图片")
    show_element(full_pic_element)
    save_pic(full_pic_element, "full")
    print("保存完整图片带滑块缺口")


def calc_distance_to_slice():
    full = Image.open(os.path.join(base, "full.png"))
    bg = Image.open(os.path.join(base, "bg.png"))

    for i in range(full.size[0]):
        for j in range(full.size[1]):
            if not compare_pixel(full, bg, i, j):
                print("距离滑块{}".format(i))
                return i


def compare_pixel(image_full, image_bg, x, y):
    bg_pixel = image_bg.load()[x, y]
    full_pixel = image_full.load()[x, y]
    threshold = 30
    if abs(bg_pixel[0] - full_pixel[0]) < threshold and abs(bg_pixel[1] - full_pixel[1]) < threshold:
        return True
    else:
        return False


def get_trace(slice_distance):
    start = 0
    trace = []
    accelerate_trace = 4 / 5 * slice_distance
    s, v0, t = 0, 0, 0.2
    while start < slice_distance:
        if start < accelerate_trace:
            a = 1.2
        else:
            a = -3.5
        s = v0 * t + 1 / 2 * a * t ** 2
        v = v0 + a * t
        v0 = v
        start += s
        trace.append(round(s))
        #trace.append(s)
    print("轨迹和{}".format(sum(trace)))
    return trace


def drag_button(trace):
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_slider_button")))
    ActionChains(web).click_and_hold(button).perform()
    for x in trace:
        ActionChains(web).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    cookies = web.get_cookies()
    print("cookies：{}".format(cookies))
    ActionChains(web).release().perform()
    time.sleep(12)
    web.quit()


if __name__ == "__main__":
    login()
    # ActionChains(web).move_by_offset()
    x = calc_distance_to_slice()
    trace = get_trace(x)
    drag_button(trace)