__author__ = 'luohua139'
func = lambda x:x
import re
from urllib import parse
import urllib.request
string ="""
  <link rel="stylesheet" href="//s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/common.0a548310.css"/>
<link rel="stylesheet" href="//s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/board-index.92a06072.css"/>
  <script crossorigin="anonymous" src="//s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/stat.88d57c80.js"></script>
  <script>if(window.devicePixelRatio >= 2) { document.write('<link rel="stylesheet" href="//s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/image-2x.8ba7074d.css"/>') }</script>
  <style>
    @font-face {
      font-family: stonefont;
      src: url('//vfile.meituan.net/colorstone/9123f6f1971a201181626f573db16e6f3428.eot');
      src: url('//vfile.meituan.net/colorstone/9123f6f1971a201181626f573db16e6f3428.eot?#iefix') format('embedded-opentype'),
           url('//vfile.meituan.net/colorstone/4ba02084c75537beea0699d5f40129622280.woff') format('woff');
    }
    """
#ret = re.findall(r"url\((.*?)\)",string)
# _font_url = re.findall(r"url\((.*?)\)",string)
# f_url = [url.replace("'","").replace("'","") for url in _font_url]
# font_url = ["https:"+url for url in f_url if url.endswith("woff")]
# res = urllib.request.urlretrieve(font_url[0],filename=font_url[0].split("/")[-1])
srt = "fafa;fafafa;ere;ytytyu;"
pp = re.sub(";","",srt)
print(pp)