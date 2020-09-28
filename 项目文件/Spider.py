#用于模拟自动化浏览
from selenium import webdriver
from time import sleep

#多进程爬虫，一个url一条进程，线程用于处理文件
import threading 
import multiprocessing
from multiprocessing import Pool
import os 

#处理Html页面
from bs4 import BeautifulSoup
import re

#用于存储最后的数据
import json


#获取全部页面的url
def get_all_url(menu_url):
    driver = webdriver.Firefox() #创建火狐对象，相当于打开浏览器
    
    driver.implicitly_wait(10) #如果没找到，进行10秒的轮询
    driver.get(menu_url) #以get方式访问url
    
    html=driver.page_source #得到页面的源码
    
    soup = BeautifulSoup(html,'html.parser')
    
    items = soup.find_all('a',class_='red') #用bs4遍历class为red的a标签
    
    for item in items:
        yield{
            item.text:'https:'+item['href']
            #用生成器返回全部的url,以字典的方式
        }
    driver.quit() #关闭这次的火狐，相当于关闭浏览器


def parse_one_page(html):
    pattern = re.compile('<dl.*?clearfix.*?src2="(.*?)"'#图片链接
                        +'.*?tit_shop">(.*?)</span>'    #标题
                        +'.*?tel_shop">(.*?)<'          #房型
                        +'.*?/i>(.*?)<i'                #面积
                        +'.*?/i>(.*?)<i'                #层数
                        +'.*?/i>(.*?)<i'                #朝向
                        +'.*?"people_name">.*?>(.*?)</' #经理人
                        +'.*?"add_shop".*?">(.*?)<'     #小区
                        +'.*?span>(.*?)<'               #位置
                        +'.*?price_right.*?b>(.*?)<'    #总价
                        +'.*?<span>(.*?)<'              #单价
                        +'.*?</dl>',re.S)

    items = re.findall(pattern,html)
    
    for item in items:
        yield{
            '图片链接':item[0].strip(),
            '标题':item[1].strip(),
            '房型':item[2].strip(),
            '面积':item[3].strip().replace('�O',''),
            '层数':item[4].strip(),
            '朝向':item[5].strip(),
            '经理人':item[6].strip(),
            '小区':item[7].strip(),
            '位置':item[8].strip(),
            '总价':item[9].strip(),
            '单价':item[10].strip().replace('�O','平米')
        }

def write_to_file(txt,content):
    with open(txt,'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close() 
 
 
def parse_one_url(city_name,url):
    txt ='./Spider_Data/'+city_name+'.txt'#文件名字
    pattern = re.compile('http.*?search.fang.com.*',re.S) #手动过滤验证码
    
    driver = webdriver.Firefox() #创建火狐对象，相当于打开浏览器
    
    driver.implicitly_wait(120) #如果没找到，进行120秒的轮询
    driver.get(url) #以get方式访问url
    
    try:
        driver.find_element_by_id('closemengceng').click()#欢迎按钮的处理，一个动态的按钮
    except:
        pass

    try:
        #第一页的处理单独拎出来
        #得到本页面的Html代码，传入解析器
        driver.implicitly_wait(120)
        for j in parse_one_page(driver.page_source):
            t = threading.Thread(target=write_to_file,args=(txt,j,))
            t.start()
            t.join() 
            
        #页数最大为100页
        for i in range(100):
            #遍历本页面的全部数据，利用点击href来实现。
            driver.find_element_by_link_text('下一页').click()
            
            try:
                while(re.match(pattern,driver.current_url)):
                    pass
                #手动绕过验证码
            except:
                pass
            
            driver.implicitly_wait(120)
            for j in parse_one_page(driver.page_source):
                t = threading.Thread(target=write_to_file,args=(txt,j,))
                t.start()
                t.join() 
            
    except:
        pass
    driver.quit() #关闭这次的火狐，相当于关闭浏览器

def open_bower(opear_city):
    for city in opear_city:
        #每三秒开启一个浏览器
        sleep(3)
        yield{
            city:opear_city[city]
        }


def main():
    menu_url="https://esf.fang.com/newsecond/esfcities.aspx"
    city_dict={}
    for url_dic in get_all_url(menu_url):
        city_dict.update(url_dic)
    
    #由于如果遍历全部的城市，即全中国二手房价格，时间就有点太久了，当然，电脑肯定是要发烫的
    #所以，就选取其中几个重要的城市来操作好了
    #一线城市：上海、北京、深圳、广州
    #二线城市：无锡市、佛山市、合肥市、大连市、福州市、厦门市、哈尔滨市、济南市、温州市、南宁市、长春市、泉州市
    #二线城市：石家庄市、贵阳市、南昌市、金华市、常州市、南通市、嘉兴市、太原市、徐州市、惠州市、珠海市、中山市
    #二线城市：台州市、烟台市、兰州市、绍兴市、扬州市
    #就操作这些城市了
    opear_city={}
    city_list=['上海','北京','深圳','广州','无锡','佛山','合肥','大连','福州','厦门','哈尔滨','济南',
    '温州','南宁','长春','泉州','石家庄','贵阳','南昌','金华','常州','南通','嘉兴','太原',
    '徐州','惠州','珠海','中山','台州','烟台','兰州','绍兴','扬州']
    for i in city_list:
        opear_city.update({i:city_dict[i]})
    
    #上海和北京的两个url要单独处理一下：
    opear_city.update({'上海':opear_city['上海'].replace('https:http:','https:')})
    opear_city.update({'北京':opear_city['北京'].replace('https:http:','https:')})
    
    pool=Pool(os.cpu_count())#定义一个大小为8的进程池
    
    for city in open_bower(opear_city):
        pool.apply_async(parse_one_url,(list(city.keys())[0],list(city.values())[0]))
    
    pool.close() #不再接受加入进程
    pool.join() #等待全部的进程结束

        
if __name__=='__main__':
    main()

