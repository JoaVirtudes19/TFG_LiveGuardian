# Generated by Django 4.1.5 on 2023-01-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detector',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
