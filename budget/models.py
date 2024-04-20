from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description