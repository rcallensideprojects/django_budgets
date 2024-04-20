from django.db import models

# Create your models here.
class Catergory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Catergory, on_delete=models.CASCADE)

    def __str__(self):
        return self.description