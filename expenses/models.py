from django.db import models

class Expense(models.Model):
    category = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.category