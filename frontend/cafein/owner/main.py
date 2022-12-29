import pandas as pd
from datetime import datetime
# 웹크롤링
from . import preprocess
from . import datacrawl
from . import model
from . import getkeywords
from multiprocessing import Process
import os

def crawl(name, number):

        cafeName = name
        cafeNum = number
        print(name,number)
        # cafeName = input("카페명을 입력하세요: ")
        # cafeNum = input("카페 전화번호를 입력하세요: ")

        # cafeName = '팡팡팡'
        # cafeNum = '053-252-2025'

        now = datetime.now()
        
        rawdata = datacrawl.collectData(cafeName, cafeNum)
        data = preprocess.processData(cafeName, rawdata)
        result = model.prediction(data)

        result.to_csv(f'.cafein/files/{cafeName}.csv', index=False, encoding='utf-8-sig')
                
        wordlist = getkeywords.getWords(result)
                
        wordlist.to_csv(f'.cafein/files/{cafeName}.csv', index=False, encoding='utf-8-sig')
     
        # 통계값 저장
        data = pd.read_csv(f'.cafein/files/{cafeName}.csv', encoding='utf-8-sig')
        
        # 전체 긍부정 
        total_pn = len(data.loc[data['sentiment']==1])/len(data)
        
        # 요소별 긍부정, 개수
        arr = ["price", "drink", "dessert", "service", "customers", "interior", "view", "parking", "trash"]
        arr_pn = [] # 긍부정 비율
        count = [] # 카테고리별 개수
        p_count = [] # 긍정 개수
        for i in arr:
                pn = len(data.loc[(data[f"{i}"]==1) & (data['sentiment']==1)])/len(data.loc[data[f"{i}"]==1])
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
        
        df_total.to_csv("df_total.csv",index=False)
        
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
        
        df_category.to_csv("df_category.csv",index=False)