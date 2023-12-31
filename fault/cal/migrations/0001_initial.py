# Generated by Django 2.2 on 2023-09-08 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_num', models.SmallIntegerField()),
                ('init_volt', models.FloatField()),
                ('init_ang', models.FloatField()),
                ('generator_p', models.FloatField()),
                ('generator_q', models.FloatField()),
                ('load_p', models.FloatField()),
                ('load_q', models.FloatField()),
                ('q_max', models.FloatField()),
                ('q_min', models.FloatField()),
                ('bus_type', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FaultCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basemva', models.SmallIntegerField()),
                ('is_flow', models.BooleanField()),
                ('fault_type', models.SmallIntegerField()),
                ('is_bus_fault', models.BooleanField()),
                ('fault_bus', models.SmallIntegerField()),
                ('fault_line_1', models.SmallIntegerField()),
                ('fault_line_2', models.SmallIntegerField()),
                ('line_percentage', models.SmallIntegerField()),
                ('impedence_R', models.FloatField()),
                ('impedence_X', models.FloatField()),
                ('is_shunt', models.BooleanField()),
                ('is_load_effect', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='LineData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_bus', models.SmallIntegerField()),
                ('from_bus', models.SmallIntegerField()),
                ('R', models.FloatField()),
                ('X', models.FloatField()),
                ('half_B', models.FloatField()),
                ('negative_R', models.FloatField()),
                ('negative_X', models.FloatField()),
                ('zero_R', models.FloatField()),
                ('zero_X', models.FloatField()),
                ('Xn', models.FloatField()),
                ('zero_half_B', models.FloatField()),
                ('line_type', models.SmallIntegerField()),
            ],
        ),
    ]
