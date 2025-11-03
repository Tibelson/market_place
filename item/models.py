from django.db import models
from django.forms import DecimalField


class Category(models.Model): 
    name = models.CharField(blank=True, null=True, max_length=255)
    class Meta:
        ordering =  ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)
    owner = models.ForeignKey('market.Vendor', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name

