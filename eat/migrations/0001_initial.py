# Generated by Django 3.2.5 on 2022-04-20 05:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='diet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_idx', models.CharField(default='none', max_length=20)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.CharField(max_length=10)),
                ('foodimage', models.ImageField(blank=True, upload_to='eat/images/%y/%m/%d/')),
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
        migrations.CreateModel(
            name='imgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedFile', models.FileField(blank=True, upload_to='Uploaded Files/%y/%m/%d/')),
                ('dateTimeOfUpload', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=10)),
                ('user_sex', models.CharField(max_length=2)),
                ('user_age', models.IntegerField(default=0)),
                ('user_height', models.FloatField(default=0.0)),
                ('user_weight', models.FloatField(default=0.0)),
                ('recommend_kcal', models.FloatField(default=2400.0)),
                ('recommend_tan', models.FloatField(default=500.0)),
                ('recommend_dang', models.FloatField(default=0.0)),
                ('recommend_ji', models.FloatField(default=40.0)),
                ('recommend_dan', models.FloatField(default=70.0)),
                ('recommend_kalsum', models.FloatField(default=700)),
                ('recommend_inn', models.FloatField(default=700)),
                ('recommend_salt', models.FloatField(default=20000)),
                ('recommend_kalum', models.FloatField(default=3500)),
                ('recommend_magnesum', models.FloatField(default=220)),
                ('recommend_cul', models.FloatField(default=15)),
                ('recommend_ayeon', models.FloatField(default=12)),
                ('recommend_kolest', models.FloatField(default=300)),
                ('recommend_transfat', models.FloatField(default=0.0)),
            ],
        ),
    ]
