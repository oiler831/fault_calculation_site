# Generated by Django 2.2 on 2023-09-13 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0012_auto_20230910_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test1', models.FloatField(blank=True)),
                ('test2', models.FloatField(blank=True)),
                ('test3', models.FloatField(blank=True)),
                ('test4', models.FloatField(blank=True)),
            ],
        ),
    ]
