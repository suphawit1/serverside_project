from django.db import models

# Create your models here.
class PurchaseOrders(models.Model):
    supplier = models.ForeignKey("product.Supplier", on_delete=models.CASCADE)
    date_ordered = models.DateField(auto_now=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseOrders_detail(models.Model):
    purchaseorders = models.ForeignKey("record.PurchaseOrders", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

class SellOrder(models.Model):
    order_date = models.DateField(auto_now=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

class SellOrder_detail(models.Model):
    sellorder = models.ForeignKey("record.SellOrder", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

class Transaction(models.Model):
    transaction_type_choice = {
        "buy":"buy",
        "sell":"sell"
    }
    sellorder = models.ForeignKey("record.SellOrder", on_delete=models.CASCADE,null=True)
    purchaseorders = models.ForeignKey("record.PurchaseOrders", on_delete=models.CASCADE,null=True)
    transaction_type = models.CharField(max_length=4,choices=transaction_type_choice)
    transaction_date = models.DateField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
