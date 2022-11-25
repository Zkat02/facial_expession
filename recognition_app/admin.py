from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile
from .models import Calculation


class Profile_Admin(admin.ModelAdmin):
    list_display = ('user','location','birth_date','photo','amount_calculations')
    search_fields = ('user',)
admin.site.register(Profile, Profile_Admin)


class Calculation_Admin(admin.ModelAdmin):
    list_display = ('user','title','calculation_image','created_at')
    search_fields = ('title','user')

    def get_photo(self, obj):
        if obj.calculation_image:
            return mark_safe(f'<img scr=" {obj.calculation_image.url}" width=75>')
        else:
            return '-'

admin.site.register(Calculation, Calculation_Admin)