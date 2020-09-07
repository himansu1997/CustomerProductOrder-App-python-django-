from django.db import models

# Create your models here.

class Product(models.Model):
    product_number = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=300,blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s"%self.product_number

class Customer(models.Model):
    product = models.ForeignKey(Product)
    first_name = models.CharField(max_length=250,null=True,blank=True)
    last_name = models.CharField(max_length=250,null=True,blank=True)
    email_id = models.CharField(max_length=250,null=True,blank=True)
    mobile_number = models.CharField(max_length=250,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return "%s"%self.first_name
    
class Order(models.Model):
    order_id = models.ForeignKey(Customer)
    billing_address = models.CharField(max_length=250)
    shipping_address = models.CharField(max_length=250)
    status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True,null=True)
    order_amount =models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    def __str__(self):
        return "%s"%self.order_id
