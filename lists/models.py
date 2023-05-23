from django.db import models



class List(models.Model):
    """список"""
    ...



# Create your models here.
class Item(models.Model):
    """элемент списка"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE,null=True, blank=True, default=None)
