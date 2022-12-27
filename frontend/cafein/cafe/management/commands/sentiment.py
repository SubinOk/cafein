import pandas as pd
from itertools import islice
from django.core.management.base import BaseCommand
from cafe.models import Cafe_sentiment,Cafe

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        batch_size = 100
        columns = ['cafe_name','total_pn', 'price_rk','price_pn','drink_rk','drink_pn','dessert_rk','dessert_pn','service_rk','service_pn','customers_rk','customers_pn','interior_rk','interior_pn','view_rk','view_pn','parking','parking_pn']
        #df = pd.total_pn('file path' names=columns, header=0)
        df = pd.read_csv('cafe/resource/통계_name.csv', names = columns, header=0)
        df = df.fillna(0)
        
        name1 = df.iloc[0,0] 
        print(name1)
        cafe = Cafe.objects.filter(name = name1)
        cafe = cafe[0].cafe_id

        objs = (Cafe_sentiment(
            total = row[1],
            price_rank = row[2],
            price_sentiment = row[3],
            drink_rank = row[4],
            drink_sentiment = row[5],
            dessert_rank = row[6],
            dessert_sentiment = row[7],
            service_rank = row[8],
            service_sentiment = row[9],
            customers_rank = row[10],
            customers_sentiment = row[11],
            interior_rank = row[12],
            interior_sentiment = row[13],
            view_rank = row[14],
            view_sentiment = row[15],
            parking_rank = row[16],
            parking_sentiment = row[17],
            cafe = cafe[0]
        ) for _, row in df.iterrows() )
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Cafe_sentiment.objects.bulk_create(batch, batch_size)