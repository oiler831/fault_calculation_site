# Generated by Django 2.2 on 2023-09-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0028_auto_20230917_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='isExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isex', models.BooleanField(default=False)),
                ('exampleNumber', models.SmallIntegerField(blank=True, default=-1, null=True)),
                ('find_ex', models.BooleanField(default=False)),
            ],
        ),
    ]
