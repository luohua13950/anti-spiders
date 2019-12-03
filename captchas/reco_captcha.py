
from captcha.image import ImageCaptcha
from  PIL import Image
from PIL import ImageFilter,ImageEnhance
from io import BytesIO,StringIO
import random
import string
import os

class Captcha():
    def __init__(self,times=1):
        self.save_dir = "..\\data\\capt\\"
        self.random_list = [ str(i) for i in range(10)]
        self.lower_case_letters = [chr(i) for i in range(97,123)]
        self.upper_case_letters = [chr(i) for i in range(ord("A"),ord("Z"))]
        self.gen_times = times
        #lower_case_letters = string.ascii_letters
        #upper_case_letters = string.ascii_uppercase.split()

    def random_captcha(self,captcha_size = 4):
        captcha = []
        for size in range(captcha_size):
            cap = random.choice(self.random_list+self.upper_case_letters)
            captcha.append(cap)

        return "".join(captcha)

    def gen_captcha(self):
        image = ImageCaptcha()
        for i in range(self.gen_times):
            captcha = self.random_captcha()
            captcha_image = Image.open(image.generate(captcha))
            filename = os.path.join(self.save_dir,captcha+".png")
            captcha_image.save(filename)
            #captcha_image.show()
            print("生成第{}张验证码:{}".format(i+1,captcha))

        #return captcha_image,captcha

    def __str__(self):
        print(self.random_list)
        return "".join(self.random_list)


    __repr__ = __str__


class IdentificationCaptcha():
    def __init__(self):
        pass




if __name__ == "__main__":
    # imag = Image.open("..\\data\\valid_code\\code2019-10-02-13-16-56.png")
    # imag = imag.convert("L")
    # imag_grey = imag.convert("1")
    # im2 = Image.new("L",imag.size,255)
    # img_filter = imag_grey.filter(ImageFilter.MedianFilter)
    # for x in range(imag.size[0]):
    #     for y in range(imag.size[1]):
    #         pix = imag.getpixel((x,y))
    #         print(pix)
    #         if pix >threshold_grey:
    #             im2.putpixel((x,y),255)
    #         else:
    #             im2.putpixel((x, y), pix)

    #img_filter.show()
    cp = Captcha(times=5000)
    cp.gen_captcha()
    #img.show()
