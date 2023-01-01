from django.contrib import admin
from cafe.models import Cafe, Cafe_image,Cafe_menu,Cafe_review,Cafe_comment,Cafe_sentiment,Cafe_keyword,Cafe_congestion,Cafe_rank,Cafe_wordcloud
# Register your models here.
admin.site.register(Cafe)
admin.site.register(Cafe_image)
admin.site.register(Cafe_menu)
admin.site.register(Cafe_review)
admin.site.register(Cafe_comment)
admin.site.register(Cafe_keyword)
admin.site.register(Cafe_sentiment)
admin.site.register(Cafe_congestion)
admin.site.register(Cafe_rank)
admin.site.register(Cafe_wordcloud)
