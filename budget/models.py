from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    hash = models.CharField(max_length=100, null=True, default=hash(''.join(['date', 'description', 'amount'])))

    def __str__(self):
        return self.description