import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

import numpy as np #用于产生数组
import jieba #用于词频统计
import re #用于文本的过滤

import os 
import multiprocessing  
from multiprocessing import Pool #多进程处理图片，计算可以快一些
from threading import Thread #控制文件夹的生成不冲突

matplotlib.rcParams['font.family']='SimHei' #中文显示

citys=['上海','北京','深圳','广州','无锡','佛山','合肥','大连','福州','厦门','哈尔滨','济南',
    '温州','南宁','长春','泉州','石家庄','贵阳','南昌','金华','常州','南通','嘉兴','太原',
    '徐州','惠州','珠海','中山','台州','烟台','兰州','绍兴','扬州']#用于读取Excel里的表格
df=pd.read_excel('../Spider_Data_Sum/All_City.xlsx',sheet_name=None) # sheet_name=None全表读取

def check_path(path):
    #用于创建文件夹
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓全国均价画图↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
def Show_Average(index):
    prices=[] #记录一二线城市均价的列表
    if(index=='总价'):
        for i in citys:
            prices.append(df[i][index].mean())
    else:
        for i in citys:
            sum=0
            count=0
            for j in df[i][index]:
                sum = sum+eval(re.search(r'\d+',j)[0])
                count = count+1
            prices.append(sum/count)
    
    plt.barh(citys,prices) #全国一二线城市均价的柱状图
    plt.title("全国一二线城市"+index+"的平均值")
    plt.ylabel("城市")
    plt.xlabel("价格" + (index=='单价'and '单位（元）' or '单位（万元）'))
    t=Thread(target=check_path,args=("../Pictures/全国/",))
    t.start()
    t.join()
    plt.savefig("../Pictures/全国/"+"全国一二线城市"+index+"的平均值"+".png",dpi=300)
    plt.show()
    
    
    if(index=='总价'):
        #均价有关的饼图
        x=0 #小于300万的占多少
        y=0 #300到600万的有多少
        z=0 #600到900万的有多少
        w=0 #大于900万的多少
        for price in prices:
            if price<300:
                x=x+1
            elif price<600:
                y=y+1
            elif price<900:
                z=z+1
            else:
                w=w+1
        labels = "小于300万","300到600万","600到900万","大于900万"
        sizes=[x,y,z,w]
        explode=(0,0.1,0,0)
        plt.pie(sizes,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=80)
        plt.axis('equal') #放平
        plt.title("全国一二线城市"+index+"的平均值的分布")
        t=Thread(target=check_path,args=("../Pictures/全国/",))
        t.start()
        t.join()
        plt.savefig("../Pictures/全国/"+"全国一二线城市"+index+"的平均值的分布"+".png",dpi=300)
        plt.show()
    elif(index=='单价'):
        #均价有关的饼图
        x=0 #小于一万的占多少
        y=0 #一万到两万的有多少
        z=0 #两万到五万的有多少
        w=0 #大于五万的多少
        for price in prices:
            if price<10**4:
                x=x+1
            elif price<2*10**4:
                y=y+1
            elif price<5*10**4:
                z=z+1
            else:
                w=w+1
        labels = "小于一万","一万到两万","两万到五万","大于五万"
        sizes=[x,y,z,w]
        explode=(0,0.1,0,0)
        plt.pie(sizes,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=80)
        plt.axis('equal') #放平
        plt.title("全国一二线城市"+index+"的平均值的分布")
        t=Thread(target=check_path,args=("../Pictures/全国/",))
        t.start()
        t.join()
        plt.savefig("../Pictures/全国/"+"全国一二线城市"+index+"的平均值的分布"+".png",dpi=300)
        plt.show()
    
    
    #全国均价的直方图
    plt.hist(prices) #全国一二线城市均价的直方图
    plt.title("全国一二线城市"+index+"的平均值的直方图")
    plt.xlabel("价格" + (index=='单价' and '单位（元）' or '单位（万元）'))
    t=Thread(target=check_path,args=("../Pictures/全国/",))
    t.start()
    t.join()
    plt.savefig("../Pictures/全国/"+"全国一二线城市"+index+"的平均值的直方图"+".png",dpi=300)
    plt.show()

# Show_Average('总价')
# Show_Average('单价')


'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑全国均价画图↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓词频统计画图↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''

def Show_30(index):
    #统计xlsx内某个项目的词语出现频率的前25
    dd=""
    for i in citys:
        for j in df[i][index]:
            dd = dd+j
    
    r='[a-zA-Z0-9\'!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘\'！[\\]^_`{|}~]+'
    dd = re.sub(r,'',dd) #过滤特殊符号，利用sub替换掉
    
    
    # dd.strip('·') #无效，已测试
    # dd.replace('·','') #无效，已测试
    
    words = jieba.lcut(dd)
    sum={} #将结巴统计好的词语：数目放在sum中
    for word in words:
        sum[word] = sum.get(word,0)+1  

    #获取小区标语前25词语的统计
    result = sorted(sum.items(),key=lambda item:item[1],reverse=True)[:25] #倒叙取前25个
    result_title=[]
    result_num=[]
    for i in result:
        result_title.append(i[0])
        result_num.append(i[1])
    plt.bar(result_title,result_num)
    plt.title("出现在"+index+"里的前25的词语")
    plt.ylabel("出行的次数")
    plt.xlabel("统计的词语")
    t=Thread(target=check_path,args=("../Pictures/全国/",))
    t.start()
    t.join()
    plt.savefig("../Pictures/全国/"+"出现在"+index+"里的前25的词语"+".png",dpi=300)
    plt.show()
    
# Show_30('小区')
# Show_30('位置')

'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑词频统计画图↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''




'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓线性关系画图↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''

def get_b1_b0(x_index,y_index):
    x_var=[]
    y_var=[]
    if(x_index=='单价' and y_index=='总价'):
        for i in citys:  
            for x,y in zip(df[i][x_index],df[i][y_index]):
                try:
                    x_var.append(eval(re.search(r'\d+',x)[0]))
                    y_var.append(y*(10**4)) #数值乘以1万，是为了和单价对应
                except:
                    pass
    elif(x_index=='层数' and y_index=='总价'):
        for i in citys:  
            for x,y in zip(df[i][x_index],df[i][y_index]):
                try:
                    if eval(re.search(r'\d+',x)[0])>100:
                        continue #排除异常值
                    x_var.append(eval(re.search(r'\d+',x)[0]))
                    y_var.append(y)
                except:
                    pass
    elif(x_index=='面积' and y_index=='总价'):
        for i in citys:  
            for x,y in zip(df[i][x_index],df[i][y_index]):
                try:
                    if eval(re.search(r'\d+',x)[0])<15:
                        continue #排除异常值
                    x_var.append(eval(re.search(r'\d+',x)[0]))
                    y_var.append(y)
                except:
                    pass
    elif(x_index=='层数' and y_index=='单价'):
        for i in citys:  
            for x,y in zip(df[i][x_index],df[i][y_index]):
                try:
                    if eval(re.search(r'\d+',x)[0])>100:
                        continue #排除异常值
                    x_var.append(eval(re.search(r'\d+',x)[0]))
                    y_var.append(eval(re.search(r'\d+',y)[0]))
                except:
                    pass
    elif(x_index=='面积' and y_index=='单价'):
        for i in citys:  
            for x,y in zip(df[i][x_index],df[i][y_index]):
                try:
                    if eval(re.search(r'\d+',x)[0])<15:
                        continue #排除异常值
                    x_var.append(eval(re.search(r'\d+',x)[0]))
                    y_var.append(eval(re.search(r'\d+',y)[0]))
                except:
                    pass

    df_show = pd.DataFrame({'x':x_var,'y':y_var})

    sum_top=0
    for x,y in zip(x_var,y_var):
        #同时遍历x,y
        sum_top = sum_top+(x-df_show['x'].mean())*(y-df_show['y'].mean())
        
    sum_low=0
    for x in x_var:
        sum_low = sum_low+((x-df_show['x'].mean())**2)
    
    return (sum_top/sum_low),df_show['y'].mean()-(sum_top/sum_low)*df_show['x'].mean()
    
#拟合的y=b0+b1x
def fx(x,b1,b0):
    #给一个预测值X，返回线性回归的预测值
    return b1*x+b0

def Show_Line(x_index,y_index):   
    b1,b0=get_b1_b0(x_index,y_index)
    x_=np.linspace(1,30,30)
    y_=[]
    for j in range(len(x_)):
        y_.append(fx(j,b1,b0))
    plt.plot(x_,y_)
    if b1>0:
        tit_show=x_index+"和"+y_index+"的线性回归(结果为正相关)(k="+str(b1)+")"
    else:
        tit_show=x_index+"和"+y_index+"的线性回归(结果为负相关)(k="+str(b1)+")"
    plt.ylabel(y_index)
    plt.xlabel(x_index)
    plt.title(tit_show)
    t=Thread(target=check_path,args=("../Pictures/全国/",))
    t.start()
    t.join()
    plt.savefig("../Pictures/全国/"+tit_show+".png",dpi=300)
    plt.show()
    
    
# Show_Line('单价','总价')
# Show_Line('层数','总价')
# Show_Line('面积','总价')
# Show_Line('层数','单价')
# Show_Line('面积','单价')
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑线性关系画图↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓（单个城市）线性关系画图↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''

def get_b1_b0_city(x_index,y_index,i):
    x_var=[]
    y_var=[]
    if(x_index=='单价' and y_index=='总价'):
        for x,y in zip(df[i][x_index],df[i][y_index]):
            try:
                x_var.append(eval(re.search(r'\d+',x)[0]))
                y_var.append(y*(10**4)) #数值乘以1万，是为了和单价对应
            except:
                pass
    elif(x_index=='层数' and y_index=='总价'):
        for x,y in zip(df[i][x_index],df[i][y_index]):
            try:
                if eval(re.search(r'\d+',x)[0])>100:
                    continue #排除异常值
                x_var.append(eval(re.search(r'\d+',x)[0]))
                y_var.append(y)
            except:
                pass
    elif(x_index=='面积' and y_index=='总价'): 
        for x,y in zip(df[i][x_index],df[i][y_index]):
            try:
                if eval(re.search(r'\d+',x)[0])<15:
                    continue #排除异常值
                x_var.append(eval(re.search(r'\d+',x)[0]))
                y_var.append(y)
            except:
                pass
    elif(x_index=='层数' and y_index=='单价'): 
        for x,y in zip(df[i][x_index],df[i][y_index]):
            try:
                if eval(re.search(r'\d+',x)[0])>100:
                    continue #排除异常值
                x_var.append(eval(re.search(r'\d+',x)[0]))
                y_var.append(eval(re.search(r'\d+',y)[0]))
            except:
                pass
    elif(x_index=='面积' and y_index=='单价'):  
        for x,y in zip(df[i][x_index],df[i][y_index]):
            try:
                if eval(re.search(r'\d+',x)[0])<15:
                    continue #排除异常值
                x_var.append(eval(re.search(r'\d+',x)[0]))
                y_var.append(eval(re.search(r'\d+',y)[0]))
            except:
                pass

    df_show = pd.DataFrame({'x':x_var,'y':y_var})

    sum_top=0
    for x,y in zip(x_var,y_var):
        #同时遍历x,y
        sum_top = sum_top+(x-df_show['x'].mean())*(y-df_show['y'].mean())
        
    sum_low=0
    for x in x_var:
        sum_low = sum_low+((x-df_show['x'].mean())**2)
    
    return (sum_top/sum_low),df_show['y'].mean()-(sum_top/sum_low)*df_show['x'].mean()
    
#拟合的y=b0+b1x
def fx_city(x,b1,b0):
    #给一个预测值X，返回线性回归的预测值
    return b1*x+b0

def Show_Line_city(x_index,y_index,city):   
    b1,b0=get_b1_b0_city(x_index,y_index,city)
    x_=np.linspace(1,30,30)
    y_=[]
    for j in range(len(x_)):
        y_.append(fx_city(j,b1,b0))
    plt.plot(x_,y_)
    if b1>0:
        tit_show=x_index+"和"+y_index+"的线性回归(结果为正相关)(k="+str(b1)+")"
    else:
        tit_show=x_index+"和"+y_index+"的线性回归(结果为负相关)(k="+str(b1)+")"
    plt.ylabel(y_index)
    plt.xlabel(x_index)
    plt.title(tit_show)
    #创建目录
    t=Thread(target=check_path,args=("../Pictures/"+city+"/",))
    t.start()
    t.join()
    plt.savefig("../Pictures/"+city+"/"+tit_show+".png",dpi=300)
    plt.show()
    
    
# Show_Line_city('单价','总价','北京')
# Show_Line_city('层数','总价','上海')
# Show_Line_city('面积','总价','深圳')
# Show_Line_city('层数','单价','广州')
# Show_Line_city('面积','单价','南昌')
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑（单个城市）线性关系画图↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

def main():
    Show_Average('总价')
    Show_Average('单价')
    Show_30('小区')
    Show_30('位置')#比较简单的计算，就不载入进程池了，太费资源了
    
    pool=Pool(os.cpu_count())#定义一个大小为8的进程池
    pool.apply_async(Show_Line,('单价','总价'))
    pool.apply_async(Show_Line,('层数','总价'))
    pool.apply_async(Show_Line,('面积','总价'))
    pool.apply_async(Show_Line,('层数','单价'))
    pool.apply_async(Show_Line,('面积','单价'))
    for i in citys:
        pool.apply_async(Show_Line_city,('单价','总价',i))
        pool.apply_async(Show_Line_city,('层数','总价',i))
        pool.apply_async(Show_Line_city,('面积','总价',i))
        pool.apply_async(Show_Line_city,('层数','单价',i))
        pool.apply_async(Show_Line_city,('面积','单价',i))
    
    pool.close()
    pool.join()
    
if __name__=='__main__':
    main()