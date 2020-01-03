import pdfplumber
import urllib
import urllib.request
from urllib.request import urlopen
from io import BytesIO
from urllib.parse import quote
import string

url = r'http://www.xxxx.com/name=中文'
url = quote(url, safe=string.printable)  # safe表示可以忽略的字符
print(url)


# path = './草单-已旋转.pdf'
path=r'http://apis.edge.customs.dev4.amiintellect.com/uploads/amiintellect-ocr/000000001/2019-06/重庆长安汽车国际销售服务有限公司/2019061400005217/single_grass/061412261189.pdf'
url=quote(path,safe=string.printable)
print(url)

url='http://apis.edge.customs.dev4.amiintellect.com/uploads/amiintellect-ocr/000000001/2019-06/%E9%87%8D%E5%BA%86%E9%95%BF%E5%AE%89%E6%B1%BD%E8%BD%A6%E5%9B%BD%E9%99%85%E9%94%80%E5%94%AE%E6%9C%8D%E5%8A%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/2019061400005217/single_grass/061412261189.pdf'


# url=BytesIO(urlopen(url))
pdf = pdfplumber.open(BytesIO(urlopen(url,'b').text()))
for page in pdf.pages:
    print(page.extract_text())