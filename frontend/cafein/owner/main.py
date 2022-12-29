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

    
        os.system(f'python manage.py runserver {8888}')
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

        result.to_csv(f'.frontend/cafein/files/{cafeName}_{now.strftime("%Y%m%d")}_result.csv', index=False, encoding='utf-8-sig')
                
        wordlist = getkeywords.getWords(result)
                
        wordlist.to_csv(f'.frontend/cafein/files/{cafeName}_{now.strftime("%Y%m%d")}_wordlist.csv', index=False, encoding='utf-8-sig')
    
