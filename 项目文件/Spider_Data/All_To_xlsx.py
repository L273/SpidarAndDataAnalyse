#由于这是个IO密集型的程序，所以，使用多线程。
from threading import Thread
import json
import pandas as pd


def write_to_xlsx(city):
    try:
        fp=open(city+'.txt','r',encoding='utf-8')
    except:
        return
   
    result_dict=[] #存储数据数列
    line=fp.readline()
    while line:
        result_dict.append(json.loads(line)) #将数据转化成字典
        line=fp.readline()

    keys=list(result_dict[0].keys()) #拿到DataFrame的索引数据
    df = pd.DataFrame()
    for key in keys:
        temp=[]
        for j in result_dict:
            temp.append(j[key])        
        df[key]=temp


    writer = pd.ExcelWriter('../Spider_Data_Xlsx/'+city+'.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()


def main():
    city_list=['上海','北京','深圳','广州','无锡','佛山','合肥','大连','福州','厦门','哈尔滨','济南',
    '温州','南宁','长春','泉州','石家庄','贵阳','南昌','金华','常州','南通','嘉兴','太原',
    '徐州','惠州','珠海','中山','台州','烟台','兰州','绍兴','扬州']
    for city in city_list:
        Thread(target=write_to_xlsx,args=(city,)).start()

if __name__=='__main__':
    main()