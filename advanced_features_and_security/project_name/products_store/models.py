from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length= 400)
    price = models.DecimalField
    category = models.TextField
