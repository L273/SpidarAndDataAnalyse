#这个程序是根据xlsx的名字
#整合所有的数据到一张xlsx的各个表中
import pandas as pd

city_list=['上海','北京','深圳','广州','无锡','佛山','合肥','大连','福州','厦门','哈尔滨','济南',
    '温州','南宁','长春','泉州','石家庄','贵阳','南昌','金华','常州','南通','嘉兴','太原',
    '徐州','惠州','珠海','中山','台州','烟台','兰州','绍兴','扬州']

writer = pd.ExcelWriter('../Spider_Data_Sum/All_City.xlsx')
for city in city_list:
    df = pd.read_excel(city+'.xlsx')#根据城市名字打开文档
    df.drop(df.columns[0],axis=1,inplace=True)#去除第一行
    df.to_excel(writer,city)#写入xlsx文件中，以city的名字作为表名
writer.save()
