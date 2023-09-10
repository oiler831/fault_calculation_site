# Generated by Django 2.2 on 2023-09-10 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0009_excelfile_find_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaultBusData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bus_No', models.SmallIntegerField()),
                ('Bus_Code', models.SmallIntegerField()),
                ('Voltage_Mag', models.FloatField()),
                ('Angle_Degree', models.FloatField()),
                ('Generator_MW', models.FloatField()),
                ('Generator_Mvar', models.FloatField()),
                ('Load_MW', models.FloatField()),
                ('Load_Mvar', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FaultLineData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_Bus', models.SmallIntegerField()),
                ('To_Bus', models.SmallIntegerField()),
                ('R', models.FloatField()),
                ('X', models.FloatField()),
                ('half_B', models.FloatField()),
                ('negative_R', models.FloatField()),
                ('negative_X', models.FloatField()),
                ('zero_R', models.FloatField()),
                ('zero_X', models.FloatField()),
                ('zero_half_B', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OtherFaultI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_Bus', models.SmallIntegerField()),
                ('To_Bus', models.SmallIntegerField()),
                ('Phase_A_Mag', models.FloatField()),
                ('Phase_A_Deg', models.FloatField()),
                ('Phase_B_Mag', models.FloatField()),
                ('Phase_B_Deg', models.FloatField()),
                ('Phase_C_Mag', models.FloatField()),
                ('Phase_C_Deg', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OtherFaultV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bus_No', models.SmallIntegerField()),
                ('Phase_A_Mag', models.FloatField()),
                ('Phase_A_Deg', models.FloatField()),
                ('Phase_B_Mag', models.FloatField()),
                ('Phase_B_Deg', models.FloatField()),
                ('Phase_C_Mag', models.FloatField()),
                ('Phase_C_Deg', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ThreeFaultI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_Bus', models.SmallIntegerField()),
                ('To_Bus', models.SmallIntegerField()),
                ('Current_Mag', models.FloatField()),
                ('Current_Deg', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ThreeFaultV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bus_No', models.SmallIntegerField()),
                ('Voltage_Mag', models.FloatField()),
                ('Voltage_Deg', models.FloatField()),
            ],
        ),
    ]
