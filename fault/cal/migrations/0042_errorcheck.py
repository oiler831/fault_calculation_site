# Generated by Django 2.2 on 2023-10-04 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0041_auto_20230924_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='errorcheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('errornum', models.IntegerField(default=0)),
                ('find_check', models.BooleanField(default=False)),
            ],
        ),
    ]
