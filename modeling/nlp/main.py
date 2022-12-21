import preprocess
import datacrawl
import model

import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    cafeName = input("카페명을 입력하세요: ")
    cafeNum = input("카페 전화번호를 입력하세요: ")

    # cafeName = '빵굽는커피공장'
    # cafeNum = '053-422-3833'

    rawdata = datacrawl.collectData(cafeName, cafeNum)
    data = preprocess.processData(cafeName, rawdata)
    result = model.prediction(data)

    now = datetime.now()
    result.to_csv(f'./modeling/nlp/data/{cafeName}_{now.strftime("%Y%m%d")}_result.csv', index=False, encoding='utf-8-sig')
    
