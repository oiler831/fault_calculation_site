# Generated by Django 2.2 on 2023-09-17 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0020_delete_faultcondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='conditionCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_not_symmetry', models.BooleanField()),
                ('is_flow', models.BooleanField()),
            ],
        ),
    ]
