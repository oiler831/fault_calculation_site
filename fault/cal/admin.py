from django.contrib import admin
from cal.models import (BusData, LineData, FaultCondition, ExcelFile,FaultBusData,FaultLineData,
                        ThreeFaultI,ThreeFaultV,OtherFaultI,OtherFaultV)

# Register your models here.
admin.site.register(BusData)
admin.site.register(LineData)
admin.site.register(FaultCondition)
admin.site.register(ExcelFile)
admin.site.register(FaultBusData)
admin.site.register(FaultLineData)
admin.site.register(ThreeFaultV)
admin.site.register(ThreeFaultI)
admin.site.register(OtherFaultV)
admin.site.register(OtherFaultI)