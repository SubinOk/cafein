import pandas as pd
from itertools import islice
from django.core.management.base import BaseCommand
from cafe.models import Cafe_sentiment,Cafe,Cafe_rank,Cafe_congestion
from django.core.files import File

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        batch_size = 100
        column_total = ['cafe_name','total_pn','total_count']
        column_category = ['category','rank','sentiment','cnt','positive_cnt']
        column = ['people']
        df_total = pd.read_csv('cafein/files/df_total.csv', names = column_total, header=0)
        df_category = pd.read_csv ('cafein/files/df_category.csv', names = column_category, header=0)
        df_total = df_total.fillna(0)
        df_category = df_category.fillna(0)
        name = df_total.iloc[0,0] 
        cafe = Cafe.objects.filter(name = name)

        #긍부정 저장
        objs = (Cafe_sentiment(
            total = row[1],
            cafe = cafe[0],
            total_count = row[2]
        ) for _, row in df_total.iterrows() )
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Cafe_sentiment.objects.bulk_create(batch, batch_size)
        sentiment = Cafe_sentiment.objects.filter(cafe = cafe[0])

        #리뷰 순위 저장
        rank = (Cafe_rank(
            category = row[0],
            rank = row[1],
            ratio = row[2],
            sentiment = sentiment[0],
            cnt = row[3],
            positive_cnt = row[4]

        ) for _, row in df_category.iterrows() )
        while True:
            batch = list(islice(rank, batch_size))
            if not batch:
                break
            Cafe_rank.objects.bulk_create(batch, batch_size)

        df = pd.read_csv('cafein/files/result/temp.csv', names = column, header=0)
        df = df.fillna(0)
        cafe = Cafe.objects.filter(name = name)
        max =cafe[0].max_occupancy

        #혼잡도 저장
        objs = (Cafe_congestion(
            congestion = (row[0] / max* 100.0),
            cafe = cafe[0],
        ) for _, row in df.iterrows() )
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Cafe_congestion.objects.bulk_create(batch, batch_size)

        # cafe_wordcloud = Cafe_wordcloud()
        
        # # Open the first image file
        # image_file_1 = open(f'media/wordcloud/{name}_0.png', 'rb')

        # # Create a Django File object
        # django_file_1 = File(image_file_1)
        # # Save the image to the first ImageField
        # cafe_wordcloud.price.save(f'{name}_0.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()
        
        # image_file_1 = open(f'media/wordcloud/{name}_1.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.drink.save(f'{name}_1.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()
        
        # image_file_1 = open(f'media/wordcloud/{name}_2.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.dessert.save(f'{name}_2.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()

        # image_file_1 = open(f'media/wordcloud/{name}_3.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.service.save(f'{name}_3.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()

        # image_file_1 = open(f'media/wordcloud/{name}_4.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.customers.save(f'{name}_4.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()

        # image_file_1 = open(f'media/wordcloud/{name}_5.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.interior.save(f'{name}_5.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()

        # image_file_1 = open(f'media/wordcloud/{name}_6.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.view.save(f'{name}_6.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()

        # image_file_1 = open(f'media/wordcloud/{name}_7.png', 'rb')
        # django_file_1 = File(image_file_1)
        # cafe_wordcloud.parking.save(f'{name}_7.png', django_file_1, save=True)
        # image_file_1.close()
        # django_file_1.close()

        # cafe = Cafe.objects.filter(name = name)
        # cafe_wordcloud.cafe = cafe[0]
        # cafe_wordcloud.save()


        
        

    


        


        

