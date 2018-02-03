import requests
from bs4 import BeautifulSoup
import time
import os

username = input("user:")
password = input("pass:")
s = requests.session()
login_data = {'username':username,'password':password}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
s.post('https://ice.xjtlu.edu.cn/login/index.php',login_data)

def findCourse():

    url = 'http://ice.xjtlu.edu.cn/my/'
    try:
        wb_data = s.get(url,headers = headers,timeout=5)
        soup = BeautifulSoup(wb_data.text,'lxml')
        courses = soup.select('a[href*="http://ice.xjtlu.edu.cn/course/view.php?id="]')
        urls = []
        for course in courses:
            urls.append(course.get("href"))
        urls = list(set(urls))
        return urls
    except urllib2.URLError as e:
        print(type(e))
    except socket.timeout as e:
        print(type(e))


def findSource(Course):
    wb_data = s.get(Course,headers = headers,timeout=5)
    soup = BeautifulSoup(wb_data.text,'lxml')
    sources = soup.select('a[href*="http://ice.xjtlu.edu.cn/mod/resource/view.php?id="]')
    temp_URLs = []
    download_URLs = []
    for source in sources:
        temp_URLs.append(source.get("href"))
        temp_URLs = list(set(temp_URLs))
    for temp in temp_URLs:
        wb_data = s.get(temp,headers = headers,timeout=5)
        soup = BeautifulSoup(wb_data.text,'lxml')
        try:
            temp_session = soup.select('''a[onclick="this.target='_blank'"]''')[0]
            download_URLs.append(temp_session.get("href"))
        except Exception as e:
            print(type(e))
        #print(download_URLs)
    return download_URLs


def downloader(url, path):
    file1 = s.get(url)
    file = open(path, 'wb')
    file.write(file1.content)
    name = path.split('/')[-1]
    print('download success: '+ name)
    file.close()

def findCourse_Name(Course):
    wb_data = s.get(Course,headers = headers,timeout=5)
    soup = BeautifulSoup(wb_data.text,'lxml')
    source = soup.select('a[href='+Course+']')[0]
    Course_Name = source.get("title")

    return Course_Name



urls = []
urls = findCourse()
for url in urls:
    Name = str(findCourse_Name(url))
    print(Name)
    print
    print

    sources_downloaded = findSource(url)
    for source_downloaded in sources_downloaded:
        file_name = str(source_downloaded.split('/')[-1])
        file_name = file_name.replace('%20',' ')
        if not os.path.exists("./"+Name+"/"):
            os.makedirs("./"+Name+"/")
        path_name = "./"+Name+"/"+file_name

        downloader(source_downloaded,path_name)
