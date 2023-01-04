import pandas as pd
# 웹크롤링
from . import preprocess
from . import datacrawl
from . import model
from . import getkeywords
import os

def crawl(name, number):
    cafeName = name
    cafeNum = number
    print(name,number)

    rawdata = datacrawl.collectData(cafeName, cafeNum)
    data = preprocess.processData(cafeName, rawdata)
    result = model.prediction(data)                
    wordlist = getkeywords.getWords(result)

    wordlist.to_csv("cafein/files/wordlist.csv",index=False, encoding='utf-8-sig')
    # 통계값 저장
    data = result
    
    # 전체 긍부정 
    total_pn = len(data.loc[data['sentiment']==1])/len(data)
    
    # 요소별 긍부정, 개수
    arr = ["price", "drink", "dessert", "service", "customers", "interior", "view", "parking", "trash"]
    arr_pn = [] # 긍부정 비율
    count = [] # 카테고리별 개수
    p_count = [] # 긍정 개수
    for i in arr:
        try:
            pn = len(data.loc[(data[f"{i}"]==1) & (data['sentiment']==1)])/len(data.loc[data[f"{i}"]==1])
            arr_pn.append(pn)
            count.append(len(data.loc[data[f"{i}"]==1]))
            p_count.append(len(data.loc[(data[f"{i}"]==1) & (data['sentiment']==1)]))
        except:
            pn = 0
            arr_pn.append(pn)
            count.append(len(data.loc[data[f"{i}"]==1]))
            p_count.append(len(data.loc[(data[f"{i}"]==1) & (data['sentiment']==1)]))

    # 요소별 랭킹 (순위가 높을수록 긍정이 높음)
    sorted_arr = sorted(arr_pn, reverse=True)

    rk =[]
    for i in arr_pn:
            rk.append(sorted_arr.index(i)+1) 
    
    # cafe_name | total_pn | total_count
    df_total = pd.DataFrame({"cafe_name":[], "total_pn":[], "total_count":[]})
    row = [f'{cafeName}', total_pn, len(data)] 
    df_total.loc[1] = row
    
    df_total.to_csv("cafein/files/df_total.csv",index=False)
    
    # category | rank | sentiment | cnt | positive_cnt
    df_category = pd.DataFrame({"category":[], "rank":[], "sentiment":[], "cnt":[], "positive_cnt":[]})
    category = ["price", "drink", "dessert", "service", "customer", "interior", "view", "parking"]

    for i in range(8):
            row = []
            row.append(category[i])
            row.append(rk[i]) 
            row.append(arr_pn[i])
            row.append(count[i])
            row.append(p_count[i])
            df_category.loc[i] = row
    
    df_category.to_csv("cafein/files/df_category.csv",index=False)

    os.system(f'python manage.py sentiment')
    os.system(f'python manage.py wordcloud')
