# Generated by Django 2.2 on 2023-09-17 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0027_auto_20230917_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='threezbussource',
            old_name='img_source',
            new_name='imag_source',
        ),
    ]