import pandas as pd
from itertools import islice
from django.core.management.base import BaseCommand
from cafe.models import Cafe_keyword

class Command(BaseCommand):
    def handle(self, *args, **options):
        batch_size = 100
        columns = ['price_word', 'price_count','drink_word','drink_count','dessert_word','dessert_count','service_word','service_count','customers_word','customers_count','interior_word','interior_count','view_word','view_count','parking_word','parking_count']
        df = pd.read_csv('cafe/resource/팡팡팡_20221222_wordlist.csv', names = columns,header=0)
        df = df.fillna(0)
        objs = (Cafe_keyword(
            price_word = row[0],
            price_count = row[1],
            drink_word = row[2],
            drink_count = row[3],
            dessert_word = row[4],
            dessert_count = row[5],
            service_word = row[6],
            service_count = row[7],
            customers_word = row[8],
            customers_count = row[9],
            interior_word = row[10],
            interior_count = row[11],
            view_word = row[12],
            view_count = row[13],
            parking_word = row[14],
            parking_count = row[15]
        ) for _, row in df.iterrows() )
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Cafe_keyword.objects.bulk_create(batch, batch_size)