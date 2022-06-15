
from django.forms import DateTimeField, ImageField
from src.settings import AUTH_USER_MODEL

from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=100)

class FuelType(models.Model):
    name = models.CharField(max_length=100)

class CarModel(models.Model):
    name = models.CharField(max_length=100)
    car_brand_id = models.ForeignKey(CarBrand,on_delete=models.CASCADE)
    fuel_type_id = models.ForeignKey(FuelType,on_delete=models.CASCADE)
    seating_capacity = models.IntegerField()
    fuel_tank_capacity = models.DecimalField(max_digits=4,decimal_places=2)

class Driver(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name =models.CharField(max_length=100)
    birthdate = models.DateField()
    is_active = models.BooleanField(default=False)
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now=True)

class Location(models.Model):
    address = models.TextField()

class Van(models.Model):
    car_model_id = models.ForeignKey(CarModel,on_delete=models.CASCADE)
    owner = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    driver_id = models.ForeignKey(Driver,on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    availability = models.BooleanField(default="False")
    date_created = models.DateTimeField(auto_now=True)

class PaymentMode(models.Model):
    method = models.CharField(max_length=100)

class Payment(models.Model):
    payment_status = models.BooleanField(default=False)
    image = ImageField()
    date_created = models.DateTimeField(auto_now=True)
    payment_method = models.ForeignKey(PaymentMode,on_delete=models.CASCADE)

class Notification(models.Model):
    from_user = models.IntegerField()
    to_user = models.IntegerField()
    text = models.TextField()
    date_time = models.DateTimeField()
    is_seen = models.BooleanField(default=False)    