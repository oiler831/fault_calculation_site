from django.db import models

# Create your models here.

class BusData(models.Model):
    bus_num =models.SmallIntegerField()
    init_volt = models.FloatField(default=1)
    init_ang = models.FloatField(default=0)
    generator_p = models.FloatField(default=0)
    generator_q = models.FloatField(default=0)
    load_p = models.FloatField(default=0)
    load_q = models.FloatField(default=0)
    q_max = models.FloatField(default=0)
    q_min = models.FloatField(default=0)
    bus_type = models.SmallIntegerField()

    def __str__(self):
        return self.bus_num


class LineData(models.Model):
    to_bus =models.SmallIntegerField()
    from_bus = models.SmallIntegerField()
    R = models.FloatField(default=0)
    X = models.FloatField(default=0)
    half_B = models.FloatField(default=0)
    negative_R = models.FloatField(default=0)
    negative_X = models.FloatField(default=0)
    zero_R = models.FloatField(default=0)
    zero_X = models.FloatField(default=0)
    Xn = models.FloatField(default=0)
    zero_half_B = models.FloatField(default=0)
    line_type = models.SmallIntegerField()

    def  __str__(self):
        return f'{self.to_bus}'"-"f'{self.from_bus}'

class FaultCondition(models.Model):
    basemva = models.SmallIntegerField()
    is_flow = models.BooleanField()
    fault_type = models.SmallIntegerField()
    is_bus_fault = models.BooleanField(default=True)
    fault_bus = models.SmallIntegerField()
    fault_line_1 = models.SmallIntegerField()
    fault_line_2 = models.SmallIntegerField()
    line_percentage = models.SmallIntegerField()
    impedence_R = models.FloatField()
    impedence_X = models.FloatField()
    is_shunt = models.BooleanField(default=False)
    is_load_effect = models.BooleanField(default=False)
