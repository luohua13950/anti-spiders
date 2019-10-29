__author__ = 'luohua139'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from fontTools.ttLib import TTFont
#font = TTFont("Microsoft YaHei.woff")
def get_font():
    font_base = TTFont("..\\data\\maoyan_data\\base.woff")
    font = TTFont("..\\data\\maoyan_data\\02cadf9173f351a5bedc5ec504805d032268.woff")
    #font_base.saveXML("T1.xml")
    #font.saveXML("4ea.xml")
    #print(font.getGlyphOrder())
    base_corresponding = {"uniEEC6":6,
                          "uniE9F5":2,
                          "uniF7EE":7,
                          "uniECA8":0,
                          "uniF0F0":3,
                          "uniEA0A":4,
                          "uniE96B":5,
                          "uniF070":9,
                          "uniECD1":1,
                          "uniE99C":8,
                        }
    base_key = list(font_base["glyf"].keys())[2:]
    key = list(font["glyf"].keys())[2:]
    print(base_key)
    print(key)
    dst_corresponding = {}
    base_coordinates = {bk:list(font_base["glyf"][bk].coordinates) for bk in base_key}
    target_coordinates = {k:list(font["glyf"][k].coordinates) for k in key}
    for bk,b_coordinates in base_coordinates.items():
        for k,coordinates in target_coordinates.items():
            if cmp(b_coordinates,coordinates,bk,k):
                dst_corresponding[k] = base_corresponding[bk]
                print(k,":",base_corresponding[bk])
                continue
def cmp(base,target,*args):
    base_len,target_len = len(base),len(target)
    if args:
        bk,k = args
    count = 0
    for bs in base:
        for tg in target:
            if abs(int(bs[0])-int(tg[0])) <20 and abs(int(bs[1])-int(tg[1])) <20:
                count +=1
    print(base_len,target_len,bk,k,count)
    return abs(count- base_len) <3  or abs(count- target_len)<3 or count >max([base_len,target_len])



if __name__ == "__main__":
    get_font()
# print(list(font["glyf"]['uniE9A4'].coordinates))
# print(base_key)
# #print(font["cmap"].getBestCmap())
# cmap_dict = {hex(int(k)):v for k,v in font["cmap"].getBestCmap().items()}
# print(cmap_dict)
# print(cmap_dict)
# glf = font.getGlyphNames()
# print(glf)
# print(font.getGlyphOrder())
# web = webdriver.Chrome("chromedriver_win32//chromedriver.exe")
# baidu = web.get("https://www.qichacha.com/")
# webelement = web.find_element_by_css_selector(".navi-btn")

#ret = web.execute_script("$(arguments[0]).click()",webelement)
#webelement.click()
#print(ret)
#print(web.page_source)
#web.quit()
#url = "https://k3.autoimg.cn/g1/M07/D2/D2/ChcCQ1sUz2mADG0HAABj9Cse-5w07..ttf"
#ret = urllib.request.urlretrieve(url,filename="ChcCQ1sUz2mADG0HAABj9Cse-5w07..ttf")
# fc = lambda x:x[0]
# a = fc([1,2,3])
# print(a)