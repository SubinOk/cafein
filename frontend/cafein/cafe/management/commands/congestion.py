import pandas as pd
from itertools import islice
from django.core.management.base import BaseCommand
from cafe.models import Cafe,Cafe_congestion
from django.core.files import File

class Command(BaseCommand):
    def handle(self, *args, **options):
        column_total = ['cafe_name','total_pn','total_count']
        column = ['people']
        df_total = pd.read_csv('cafein/files/df_total.csv', names = column_total, header=0)
        name = df_total.iloc[0,0]
        df = pd.read_csv('cafein/files/result/temp.csv', names = column, header=0)
        df = df.fillna(0)
        cafe = Cafe.objects.filter(name = name)
        congestion = Cafe_congestion.objects.filter(cafe__in = cafe)
        cong = df.iloc[0,0]
        max =cafe[0].max_occupancy
        
       #혼잡도 값 수정
        congestion_value = cong / max* 100.0
        congestion.congestion= congestion_value
        congestion.save()






        