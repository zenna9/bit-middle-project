# Generated by Django 4.0.4 on 2022-06-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(default='none', max_length=20)),
                ('basic_g', models.FloatField(default=0.0)),
                ('kcal', models.FloatField(default=0.0)),
                ('tan', models.FloatField(default=0.0)),
                ('dang', models.FloatField(default=0.0)),
                ('ji', models.FloatField(default=0.0)),
                ('dan', models.FloatField(default=0.0)),
                ('kalsum', models.FloatField(default=0.0)),
                ('inn', models.FloatField(default=0.0)),
                ('salt', models.FloatField(default=0.0)),
                ('kalum', models.FloatField(default=0.0)),
                ('magnesum', models.FloatField(default=0.0)),
                ('chul', models.FloatField(default=0.0)),
                ('ayeon', models.FloatField(default=0.0)),
                ('kolest', models.FloatField(default=0.0)),
                ('transfat', models.FloatField(default=0.0)),
            ],
        ),
    ]
