from django.db import models
from market.models import Vendor

class Category(models.Model): 
    name = models.CharField(blank=True, null=True, max_length=255)
    class Meta:
        ordering =  ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(blank = True, null = True)
    price = models.FloatField()
    is_sold = models.BooleanField()
    owner = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name

