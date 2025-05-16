from django.contrib import admin
from .models import Person, Hisab

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Hisab)
class HisabAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'price', 'person', 'if_online', 'platform', 'date')
    list_filter = ('if_online', 'platform', 'person')
    search_fields = ('item', 'description')
