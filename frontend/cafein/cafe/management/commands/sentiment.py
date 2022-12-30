import pandas as pd
from itertools import islice
from django.core.management.base import BaseCommand
from cafe.models import Cafe_sentiment,Cafe,Cafe_rank,Cafe_congestion

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
        #name = '팡팡팡'
        df = df.fillna(0)
        cafe = Cafe.objects.filter(name = name)
        max =cafe[0].max_occupancy
        objs = (Cafe_congestion(
            congestion = (row[0] / max* 100.0),
            cafe = cafe[0],
        ) for _, row in df.iterrows() )
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Cafe_congestion.objects.bulk_create(batch, batch_size)