# Generated by Django 2.2 on 2023-09-22 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0032_othersequencei_othersequencev'),
    ]

    operations = [
        migrations.AddField(
            model_name='busdata',
            name='Bus_Code',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Generator_MW',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Generator_Mvar',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Load_MW',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Load_Mvar',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Qmax',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Qmin',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Voltage_Deg',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='busdata',
            name='Voltage_Mag',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='linedata',
            name='R',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='linedata',
            name='X',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='linedata',
            name='Xn',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='linedata',
            name='half_B',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='linedata',
            name='line_type',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='linedata',
            name='negative_R',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='linedata',
            name='negative_X',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='linedata',
            name='zero_R',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='linedata',
            name='zero_X',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='linedata',
            name='zero_half_B',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]