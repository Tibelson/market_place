from django.contrib.auth.models import AbstractUser
from django.db import models
from item.models import Item

class User(AbstractUser):
    ROLE_CHOICES = (
        ('VENDORS','vendors'),
        ('customer', 'CUSTOMER')
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name
    

class Vendor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='vendor_profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.store_name
    
# class Product(models.Model):
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
#     product_name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.PositiveIntegerField()
#     product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)

#     def __str__(self):
#         return self.product_name
    
class Order(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name} for {self.customer_name}"
    

class Chat(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat with {self.customer_name} at {self.timestamp}"

class Subscription(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user  = models.ForeignKey('User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Subscription for {self.vendor.store_name} by {self.user.username}"