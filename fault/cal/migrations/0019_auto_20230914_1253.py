# Generated by Django 2.2 on 2023-09-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0018_auto_20230914_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='input_excel'),
        ),
        migrations.AlterField(
            model_name='excelfile',
            name='find_file',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
