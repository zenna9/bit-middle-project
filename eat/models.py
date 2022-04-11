from django.db import models
from datetime import datetime

class login(models.Model):
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user_name = models.CharField(max_length=10)
    user_sex = models.CharField(max_length=2)
    user_age = models.IntegerField(default=0)
    user_height = models.FloatField(default=0.0)
    user_weight = models.FloatField(default=0.0)
    recommend_kcal = models.FloatField(default=0.0)

class diet(models.Model) :
    user_idx = models.CharField(max_length=20, default="none")
    date = models.DateField(default=datetime.now())
    time = models.CharField(max_length=10)
    foodimage = models.ImageField(upload_to='eat/images/%y/%m/%d/', blank=True)
    kcal = models.FloatField(default=0.0)
    tan = models.FloatField(default=0.0)
    dang = models.FloatField(default=0.0)
    ji = models.FloatField(default=0.0)
    dan = models.FloatField(default=0.0)
    kalsum = models.FloatField(default=0.0)
    inn = models.FloatField(default=0.0)
    salt = models.FloatField(default=0.0)
    kalum = models.FloatField(default=0.0)
    magnesum = models.FloatField(default=0.0)
    chul = models.FloatField(default=0.0)
    ayeon = models.FloatField(default=0.0)
    kolest = models.FloatField(default=0.0)
    transfat = models.FloatField(default=0.0)

class imgs(models.Model) :
    foodimage = models.ImageField(upload_to='eat/images/%y/%m/%d/', blank=True)