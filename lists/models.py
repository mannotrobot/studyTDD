from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse



class List(models.Model):
    """список"""

    def get_absolute_url(self):
        """получить абсолютный url"""
        return reverse("view_list", args=[self.id])



# Create your models here.
class Item(models.Model):
    """элемент списка"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True, blank=True, default=None)


    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


    def __str__(self):
        return self.text
