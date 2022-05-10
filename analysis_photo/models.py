from django.db import models

class menu(models.Model) :
    food_name = models.CharField(max_length=20, default="none")
    basic_g = models.FloatField(default=0.0)
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
