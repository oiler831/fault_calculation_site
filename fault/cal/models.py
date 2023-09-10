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
    to_find = models.BooleanField(default=False)

class ExcelFile(models.Model):
    file = models.FileField(upload_to="input_excel")
    find_file = models.BooleanField(default=False)


class FaultBusData(models.Model):
    Bus_No = models.SmallIntegerField()
    Bus_Code = models.SmallIntegerField()
    Voltage_Mag = models.FloatField()
    Voltage_Deg = models.FloatField()
    Generator_MW = models.FloatField()
    Generator_Mvar = models.FloatField()
    Load_MW = models.FloatField()
    Load_Mvar = models.FloatField()


class FaultLineData(models.Model):
    From_Bus = models.SmallIntegerField()
    To_Bus = models.SmallIntegerField()
    R = models.FloatField()
    X = models.FloatField()
    half_B = models.FloatField()
    negative_R = models.FloatField()
    negative_X = models.FloatField()
    zero_R = models.FloatField()
    zero_X = models.FloatField()
    zero_half_B = models.FloatField()


class ThreeFaultV(models.Model):
    Bus_No = models.SmallIntegerField()
    Voltage_Mag = models.FloatField()
    Voltage_Deg = models.FloatField()


class ThreeFaultI(models.Model):
    From_Bus = models.SmallIntegerField()
    To_Bus = models.SmallIntegerField()
    Current_Mag = models.FloatField()
    Current_Deg = models.FloatField()


class OtherFaultV(models.Model):
    Bus_No = models.SmallIntegerField()
    Phase_A_Mag = models.FloatField()
    Phase_A_Deg = models.FloatField()
    Phase_B_Mag = models.FloatField()
    Phase_B_Deg = models.FloatField()
    Phase_C_Mag = models.FloatField()
    Phase_C_Deg = models.FloatField()


class OtherFaultI(models.Model):
    From_Bus = models.SmallIntegerField()
    To_Bus = models.SmallIntegerField()
    Phase_A_Mag = models.FloatField()
    Phase_A_Deg = models.FloatField()
    Phase_B_Mag = models.FloatField()
    Phase_B_Deg = models.FloatField()
    Phase_C_Mag = models.FloatField()
    Phase_C_Deg = models.FloatField()