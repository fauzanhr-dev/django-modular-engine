from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return f"{self.name}"