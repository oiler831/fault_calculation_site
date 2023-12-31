# Generated by Django 2.2 on 2023-09-17 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0023_faultcondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreeZbus',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ThreeZbusSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.FloatField()),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cal.ThreeZbus')),
            ],
        ),
    ]
