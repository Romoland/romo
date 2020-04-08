import os
from os import path
import urllib.parse
import requests
from bs4 import BeautifulSoup

# 声明基础变量
dirPath = path.join(path.abspath(path.dirname(__file__)), 'data')
base_url = 'http://www.hebeu.edu.cn/notice/'

# 声明request请求的headers
headers = {
    "Host": "www.hebeu.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://www.hebeu.edu.cn/",
}

# 创建文件夹函数, 如果已经存在则不创建
def createDir(dir_path):
    if dir_path != None and not path.exists(dir_path):
        os.makedirs(dir_path)

# http://www.hebeu.edu.cn/notice/2017.xml
def startJob(xml_name='2020.xml'):
    # 请求这个地址, 获取服务端的响应数据
    url = urllib.parse.urljoin(base_url, xml_name)
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    # 解析返回的文本内容
    soup = BeautifulSoup(r.text, 'html.parser')
    # 寻找所有的data节点
    datas = soup.find_all('data')
    # 遍历找到的data节点
    for data in datas:
        # 寻找当前data节点下的title节点
        title = data.find('title').text.strip().replace('"', '').replace('\r\n', '').replace('/', '-')
        # 寻找当前data节点下的url节点
        url = data.find('url').text.strip()
        # 寻找当前data节点下的date节点
        date = data.find('date').text.strip()

        # 从中获取到年份
        year = date.split('-')[0]
        # 创建对应年份的文件夹
        createDir(path.join(dirPath, year))

        # 获取对应的页面数据
        url = urllib.parse.urljoin(base_url, url)
        res = requests.get(url, headers=headers)
        res.encoding = 'gb2312'
        # 把服务端返回的数据依次按照年份写到不同的文件夹里, 文件名为: title.html
        fileName = title + '.html'
        with open(path.join(dirPath, year, fileName), mode='w',
                  encoding=res.encoding, errors='ignore') as f:
            f.write(res.text)


for year in range(2017, 2021):
    startJob(str(year) + '.xml')
    print(str(year) + ' has been completed!')
    
