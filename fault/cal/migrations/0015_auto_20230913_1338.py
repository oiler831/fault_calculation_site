# Generated by Django 2.2 on 2023-09-13 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0014_auto_20230913_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='test2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='test3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='test4',
            field=models.FloatField(blank=True, null=True),
        ),
    ]