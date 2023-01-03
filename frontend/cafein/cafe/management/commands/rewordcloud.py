from wordcloud import WordCloud
from django.core.management.base import BaseCommand
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cafe.models import Cafe,Cafe_wordcloud
from io import BytesIO

class Command(BaseCommand):
    def handle(self, *args, **options):
        column_total = ['cafe_name','total_pn','total_count']
        wordlist = pd.read_csv('cafein/files/wordlist.csv', header=0)
        df_total = pd.read_csv('cafein/files/df_total.csv', names = column_total, header=0)
        cafeName = df_total.iloc[0,0]
        cafeName = cafeName.replace("_", " ") 
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

        #디비 삭제
        cafe = Cafe.objects.filter(name = cafeName)[0]
        cafe_wordcloud=Cafe_wordcloud.objects.filter(cafe =cafe)[0]
        cafe_wordcloud.delete()
        cafe_wordcloud = Cafe_wordcloud()
        for i in range(8):
                wordCloud = WordCloud(
                font_path = "H2HDRM", # 폰트 지정
                width = 400, # 워드 클라우드의 너비 지정
                height = 400, # 워드클라우드의 높이 지정
                max_font_size=100, # 가장 빈도수가 높은 단어의 폰트 사이즈 지정
                background_color = '#f8f8f8',# 배경색 지정
                colormap= cmap
                ).generate_from_frequencies(wc_list[i]) # 워드 클라우드 빈도수 지정
                image_file = BytesIO()
                wordCloud.to_image().save(image_file, 'PNG')
                image_file.seek(0)
                if i == 0:
                    cafe_wordcloud.price.save(f'{cafeName}_0.png', image_file, save=True)
                elif i == 1:
                    cafe_wordcloud.drink.save(f'{cafeName}_1.png', image_file, save=True)
                elif i == 2:
                    cafe_wordcloud.dessert.save(f'{cafeName}_2.png', image_file, save=True)
                elif i == 3:
                    cafe_wordcloud.service.save(f'{cafeName}_3.png', image_file, save=True)
                elif i == 4:
                    cafe_wordcloud.customers.save(f'{cafeName}_4.png', image_file, save=True)
                elif i == 5:
                    cafe_wordcloud.interior.save(f'{cafeName}_5.png', image_file, save=True)
                elif i == 6:
                    cafe_wordcloud.view.save(f'{cafeName}_6.png', image_file, save=True)  
                else :
                    cafe_wordcloud.parking.save(f'{cafeName}_7.png', image_file, save=True)  
                    cafe = Cafe.objects.filter(name = cafeName)
                    cafe_wordcloud.cafe = cafe[0]
                    cafe_wordcloud.save()
                            
        
