from django.db import models

# Create your models here.

class BusData(models.Model):
    bus_num =models.SmallIntegerField()

class LineData(models.Model):
    to_bus =models.SmallIntegerField()
    from_bus = models.SmallIntegerField()

class FaultCondition(models.Model):
    basemva = models.SmallIntegerField()
    is_flow = models.BooleanField()
    fault_type = models.SmallIntegerField()
    is_bus_fault = models.BooleanField(default=True)
    fault_bus = models.SmallIntegerField(null=True)
    fault_line_1 = models.SmallIntegerField(null=True)
    fault_line_2 = models.SmallIntegerField(null=True)
    line_percentage = models.SmallIntegerField(null=True)
    impedence_R = models.FloatField()
    impedence_X = models.FloatField()
    is_shunt = models.BooleanField(default=False)
    is_load_effect = models.BooleanField(default=False)

class ExcelFile(models.Model):
    file = models.FileField(upload_to="input_excel")
