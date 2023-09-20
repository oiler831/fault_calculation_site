# Generated by Django 2.2 on 2023-09-19 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0029_isexample'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faultbusdata',
            name='Bus_Code',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultbusdata',
            name='Generator_MW',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultbusdata',
            name='Generator_Mvar',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultbusdata',
            name='Load_MW',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultbusdata',
            name='Load_Mvar',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultlinedata',
            name='negative_R',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultlinedata',
            name='negative_X',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultlinedata',
            name='zero_R',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultlinedata',
            name='zero_X',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='faultlinedata',
            name='zero_half_B',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
