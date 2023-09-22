from django.contrib import admin
from cal.models import (BusData, LineData, FaultCondition, ExcelFile,FaultBusData,FaultLineData,
                        ThreeFaultI,ThreeFaultV,OtherFaultI,OtherFaultV,conditionCheck, ThreeZbus,ThreeZbusSource,
                        OtherZbus,OtherZbusSource,negativeZbusSource,zeroZbusSource,isExample,OthersequenceI,OthersequenceV)

# Register your models here.
admin.site.register(BusData)
admin.site.register(LineData)
admin.site.register(ExcelFile)
admin.site.register(isExample)
admin.site.register(conditionCheck)
admin.site.register(FaultCondition)
admin.site.register(FaultBusData)
admin.site.register(FaultLineData)
admin.site.register(ThreeFaultV)
admin.site.register(ThreeFaultI)
admin.site.register(OtherFaultV)
admin.site.register(OtherFaultI)
admin.site.register(ThreeZbus)
admin.site.register(ThreeZbusSource)
admin.site.register(OtherZbus)
admin.site.register(OtherZbusSource)
admin.site.register(negativeZbusSource)
admin.site.register(zeroZbusSource)
admin.site.register(OthersequenceV)
admin.site.register(OthersequenceI)