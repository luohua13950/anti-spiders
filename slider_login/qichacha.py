__author__ = 'luohua139'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import time
from fontTools.ttLib import TTFont
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from utils.CTools import Common
from selenium.webdriver import ChromeOptions

class QiXX(object):
    def __init__(self):
        self.url = "https://www.qichacha.com/user_login"
        self.options = ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.webdriver = webdriver.Chrome(executable_path="..\\data\\webdriver\\chromedriver.exe",options=self.options)
        self.wait= WebDriverWait(self.webdriver, timeout=15)
        self.username = "18101889581"
        self.password = "xiangcao2717"
        self.slip_width = 320
        self.step = 10
        self.cm = Common()
        self.webdriver.maximize_window()

    def get_login_element(self):
        self.webdriver.get(self.url)
        password_login = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "密码登录")))
        password_login.click()
        time.sleep(2)
        try:
            username = self.wait.until(EC.presence_of_element_located((By.ID, "nameNormal")))
            password = self.wait.until(EC.presence_of_element_located((By.ID, "pwdNormal")))
            username.send_keys(self.username)
            password.send_keys(self.password)
        except:
            self.webdriver.quit()

    def drag_button(self):
        self.get_login_element()
        button = self.wait.until(EC.presence_of_element_located((By.ID, "nc_1_n1z")))
        actions = ActionChains(self.webdriver)
        actions.click_and_hold(button).perform()
        trace = [50,60,40,70,30,20,10,20,10,10,40]
        for x in trace:
            time.sleep(0.3)
            actions.move_by_offset(xoffset=x,yoffset=0).perform()
            actions = ActionChains(self.webdriver)
        time.sleep(1)
        actions.release().perform()
        time.sleep(30)
        self.webdriver.quit()


    @property
    def get_trace(self):
        trace = self.cm.get_trace(self.slip_width)
        return trace


if __name__ == "__main__":
    qxx = QiXX()
    qxx.drag_button()
