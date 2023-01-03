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
        cong = df.iloc[0,0]
        max =cafe[0].max_occupancy
        congestion = Cafe_congestion.objects.filter(cafe = cafe)
        #혼잡도 값 수정
        congestion[0].congestion = (cong / max* 100.0)
        congestion[0].save()





        