from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Supplier(models.Model):
    name = models.CharField(max_length=25)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=75)

    def __str__(self):
        return self.name
