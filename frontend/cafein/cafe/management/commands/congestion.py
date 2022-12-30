import pandas as pd
from itertools import islice
from django.core.management.base import BaseCommand
from cafe.models import Cafe_congestion,Cafe

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        batch_size = 100
        column = ['people']
        
        #df = pd.total_pn('file path' names=columns, header=0)
        df = pd.read_csv('cafein/files/result/temp.csv', names = column, header=0)
        name = '팡팡팡'
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
        