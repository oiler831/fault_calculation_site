from django.contrib import admin
from cal.models import BusData, LineData, FaultCondition

# Register your models here.
admin.site.register(BusData)
admin.site.register(LineData)
admin.site.register(FaultCondition)