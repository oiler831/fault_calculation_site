from django.db import models

# Create your models here.

class BusData(models.Model):
    bus_num =models.SmallIntegerField()

class LineData(models.Model):
    to_bus =models.SmallIntegerField()
    from_bus = models.SmallIntegerField()

class conditionCheck(models.Model):
    is_not_symmetry = models.BooleanField()
    is_flow = models.BooleanField()
    find_con = models.BooleanField(default=False)

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
    file = models.FileField(upload_to="input_excel",null=True,blank=True)
    find_file = models.BooleanField(default=False,null=True,blank=True)

class isExample(models.Model):
    isex = models.BooleanField(default=False)
    exampleNumber = models.SmallIntegerField(default=-1,null=True,blank=True)
    find_ex = models.BooleanField(default=False)


class FaultBusData(models.Model):
    Bus_No = models.SmallIntegerField()
    Bus_Code = models.SmallIntegerField(default=0,null=True,blank=True)
    Voltage_Mag = models.FloatField()
    Voltage_Deg = models.FloatField()
    Generator_MW = models.FloatField(default=0,null=True,blank=True)
    Generator_Mvar = models.FloatField(default=0,null=True,blank=True)
    Load_MW = models.FloatField(default=0,null=True,blank=True)
    Load_Mvar = models.FloatField(default=0,null=True,blank=True)


class FaultLineData(models.Model):
    From_Bus = models.SmallIntegerField()
    To_Bus = models.SmallIntegerField()
    R = models.FloatField()
    X = models.FloatField()
    half_B = models.FloatField()
    negative_R = models.FloatField(default=0,null=True,blank=True)
    negative_X = models.FloatField(default=0,null=True,blank=True)
    zero_R = models.FloatField(default=0,null=True,blank=True)
    zero_X = models.FloatField(default=0,null=True,blank=True)
    zero_half_B = models.FloatField(default=0,null=True,blank=True)


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

class ThreeZbus(models.Model): 
    check = models.SmallIntegerField(default=0)


class ThreeZbusSource(models.Model):
    row = models.ForeignKey("ThreeZbus", on_delete=models.CASCADE)
    real_source = models.FloatField(default=0)
    imag_source = models.FloatField(default=0)
    y_real_source = models.FloatField(default=0)
    y_imag_source = models.FloatField(default=0)

class OtherZbus(models.Model): 
    check = models.SmallIntegerField(default=0)

class OtherZbusSource(models.Model):
    row = models.ForeignKey("OtherZbus", on_delete=models.CASCADE)
    real_source = models.FloatField(default=0)
    imag_source = models.FloatField(default=0)
    y_real_source = models.FloatField(default=0)
    y_imag_source = models.FloatField(default=0)

class negativeZbusSource(models.Model):
    row = models.ForeignKey("OtherZbus", on_delete=models.CASCADE)
    real_source = models.FloatField(default=0)
    imag_source = models.FloatField(default=0)
    y_real_source = models.FloatField(default=0)
    y_imag_source = models.FloatField(default=0)

class zeroZbusSource(models.Model):
    row = models.ForeignKey("OtherZbus", on_delete=models.CASCADE)
    real_source = models.FloatField(default=0)
    imag_source = models.FloatField(default=0)
    y_real_source = models.FloatField(default=0)
    y_imag_source = models.FloatField(default=0)