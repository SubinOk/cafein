import pandas as pd
from datetime import datetime
# 웹크롤링
from . import preprocess
from . import datacrawl
from . import model
from . import getkeywords
from multiprocessing import Process
import os

# 워드클라우드
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def crawl(name, number):

        cafeName = name
        cafeNum = number
        print(name,number)

        rawdata = datacrawl.collectData(cafeName, cafeNum)
        data = preprocess.processData(cafeName, rawdata)
        result = model.prediction(data)

                
        wordlist = getkeywords.getWords(result)
                
     
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

        # 워드클라우드
        data = wordlist 
        
        data = data.fillna(0)
        
        # 카테고리별 df -> wc
        arr = ["price", "drink", "dessert", "service", "customers", "interior", "view", "parking"]
        wc_list =[]

        for i in arr:
                df = data[[f'{i}_word', f'{i}_count']]
                wc = df.set_index(f'{i}_word').to_dict()[f'{i}_count']
                wc_list.append(wc)
        
        from matplotlib.colors import LinearSegmentedColormap
        colors = ['#744C2E', '#583A23', '#825634', '#DFC4AF','#C39068']
        cmap = LinearSegmentedColormap.from_list('my_cmap',colors,gamma=2)

        for i in range(8):
                wordCloud = WordCloud(
                font_path = "H2HDRM", # 폰트 지정
                width = 400, # 워드 클라우드의 너비 지정
                height = 400, # 워드클라우드의 높이 지정
                max_font_size=100, # 가장 빈도수가 높은 단어의 폰트 사이즈 지정
                background_color = 'white',# 배경색 지정
                colormap= cmap
                ).generate_from_frequencies(wc_list[i]) # 워드 클라우드 빈도수 지정
                
                wordCloud.to_file(filename=f"cafein/files/wordcloud{cafeName}_{i}.png")