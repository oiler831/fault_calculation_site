# Generated by Django 2.2 on 2023-09-14 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0017_testzbus_testzbuscolumn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testzbuscolumn',
            name='test_id',
        ),
        migrations.DeleteModel(
            name='testzbus',
        ),
        migrations.DeleteModel(
            name='testzbuscolumn',
        ),
    ]
