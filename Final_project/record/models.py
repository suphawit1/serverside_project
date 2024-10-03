from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ManyToManyField(Category)

class Supplier(models.Model):
    name = models.CharField(max_length=25)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=75)

class PurchaseOrders(models.Model):
    supplier = models.ForeignKey("record.Supplier", on_delete=models.CASCADE)
    date_ordered = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseOrders_detail(models.Model):
    purchaseorders = models.ForeignKey("record.PurchaseOrders", on_delete=models.CASCADE)
    product = models.ForeignKey("record.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

class SellOrder(models.Model):
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class SellOrder_detail(models.Model):
    sellorder = models.ForeignKey("record.SellOrder", on_delete=models.CASCADE)
    product = models.ForeignKey("record.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    transaction_type_choice = {
        "buy":"buy",
        "sell":"sell"
    }
    sellorder = models.ForeignKey("record.SellOrder", on_delete=models.CASCADE,null=True)
    purchaseorders = models.ForeignKey("record.PurchaseOrders", on_delete=models.CASCADE,null=True)
    transaction_type = models.CharField(max_length=4,choices=transaction_type_choice)
    transaction_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
