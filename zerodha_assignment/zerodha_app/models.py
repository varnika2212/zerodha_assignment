from django.db import models

# Create your models here.
class Item(models.Model):
    code = models.IntegerField(max_length=100)
    name = models.CharField(max_length=100)
    date= models.DateField(auto_now_add=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)

    def __str__(self):
         return self.name
