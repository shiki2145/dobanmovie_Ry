# -*- coding = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式——进行文字匹配
import urllib.request,urllib.error  # 使用URL，获取网页数据
import json

def main():
    baseurl = "https://movie.douban.com/top250?start="
    DataLists = getData(baseurl)
    for datalist in DataLists:
        saveData(datalist)

    print("完成！")

findrank = re.compile(r'<em class="">(.*?)</em>')#电影排名
findLink = re.compile(r'<a href="(.*?)">')#电影详情页链接
findMark = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')#电影评分
findnum = re.compile(r'<span>(.*?)评价</span>')#电影评分人数
findImg = re.compile(r'<img.*src="(.*?)"',re.S)#电影封面图片地址
findName = re.compile(r'<span class="title">(.*?)</span>')#电影名
findComt = re.compile(r'<span class="inq">(.*?)</span>')#电影简介
findbd = re.compile('<div class="bd">(.*?)导演: (.*?)\xa0\xa0\xa0主演: (.*?)<br/>\n(.*) (.*?)\xa0/\xa0(.*?)\xa0/\xa0(.*?)\n',re.S)
findsum = re.compile('<span property="v:summary">\n(.*?)</span>',re.S)
findsum2 = re.compile('<span class="" property="v:summary">(.*?)</span>',re.S)
findreview = re.compile('<span class="short">(.*?)</span>',re.S)

def getridof(summary):
    try:
        summary = summary.replace("\n", "")
    except:
        summary = summary

def getridof2(summary):
    try:
        summary = summary.replace(u'\u3000',u'')
    except:
        summary = summary
# 爬取网页
def getData(baseurl):
    baseurl = "https://movie.douban.com/top250?start="
    datalists = []
    x = 0
    for i in range (0,10):
        url = baseurl + str(i*25)
        html = askURL(url)
    #逐一进行解析
        soup = BeautifulSoup(html,"html.parser")
        # print(soup)
        # exit(1)
        for item in soup.find_all('div',class_="item"):
            x = x + 1
            data = []
            item = str(item)
            Img = "电影图片链接："+re.findall(findImg,item)[0]
            data.append(Img)
            # print(Img)
            link = "电影详情页链接："+re.findall(findLink,item)[0]
            data.append(link)
            # print(link)
            Links = re.findall(findLink, item)[0]
            Rank = "电影排名："+re.findall(findrank, item)[0]
            data.append(Rank)
            # print(Rank)
            Mark = "电影评分："+re.findall(findMark,item)[0]
            data.append(Mark)
            # print(Mark)
            Num = "电影评分人数："+re.findall(findnum,item)[0]
            data.append(Num)
            # print(Num)
            Name = "电影名称："+re.findall(findName,item)[0]
            data.append(Name)
            # print(Name)
            Comt = re.findall(findComt,item)
            # print(Comt)
            # exit(1)
            if(len(Comt) == 0):
                data.append("电影简介："+' ')
            if(len(Comt) != 0):
                Comt = "电影简介："+Comt[0].replace("。","")
                data.append(Comt)
            else:
                data.append("电影简介："+' ')
            DB = re.findall(findbd,item)
            if (len(DB) == 0):
                DB = ('缺失','缺失','缺失','缺失','缺失','缺失','缺失')
            else:
                DB = DB[0]
            Dire = "导演："+DB[1]
            # print(Dire)
            data.append(Dire)
            # print(Dire)
            Act = "主演："+DB[2]
            data.append(Act)
            # print(Act)
            Time = "上映时间："+DB[4]
            data.append(Time)
            # print(Time)
            Country = "国家："+DB[5]
            data.append(Country)
            # print(Country)
            Type = "电影类型："+DB[6]
            data.append(Type)
            # print(Type)
            # exit(1)
            # print(datalists[0])
            # exit(1)
            getdetail(Links,data)
            # print(datalists)
            datalists.append(data)
            print("完成第" + str(x) + "条")
    return datalists

def getdetail(baseurl,data):
    url = baseurl
    html = askURL(url)
    # 逐一进行解析
    soup = BeautifulSoup(html, "html.parser")
    for info in soup.find_all('div', class_="related-info"):
        info = str(info)
        # print(len(re.findall(findsum2, info)))
        if len(re.findall(findsum, info)) == 0:
            # print(re.findall(findsum2,info))
            Sumy = re.findall(findsum2, info)[0].replace(" ", "")
            getridof(Sumy)
            getridof2(Sumy)
            # print(Sumy)
        else:
            # print(re.findall(findsum,info))
            Sumy = re.findall(findsum, info)[0].replace(" ", "")
            getridof(Sumy)
            getridof2(Sumy)
            # print(Sumy)
        data.append(Sumy)
        # print(re.findall(findsum,info))
        # print(info)
        # print(Sumy)
        # exit(1)
    i = 0
    for comment in soup.find_all('div', class_="comment"):
        comment = str(comment)
        i = i + 1
        review = "短评"+str(i)+": "+re.findall(findreview,comment)[0]
        # print(review)
        # print(comment)
        data.append(review)
        if i >= 3:
            break
    return 0

def askURL(url):
    head = {"User-Agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 99.0.4844.74Safari / 537.36"}
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

# 3.保存数据
def saveData(datalist):
    with open('.\\result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(datalist, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()