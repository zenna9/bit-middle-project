# Generated by Django 4.0.4 on 2022-05-10 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis_photo', '0003_auto_20220510_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
