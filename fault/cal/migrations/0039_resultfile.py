# Generated by Django 2.2 on 2023-09-24 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0038_delete_resultfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='resultfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfile', models.FileField(upload_to='result')),
            ],
        ),
    ]