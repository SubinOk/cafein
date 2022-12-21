from django.contrib import admin
from cafe.models import Cafe, Cafe_image,Cafe_menu,Cafe_review,Cafe_comment
# Register your models here.
admin.site.register(Cafe)
admin.site.register(Cafe_image)
admin.site.register(Cafe_menu)
admin.site.register(Cafe_review)
admin.site.register(Cafe_comment)