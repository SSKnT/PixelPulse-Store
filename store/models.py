from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name=models.TextField()
    description= models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CATEGORY_CHOICES = [
        ('AMD', 'AMD'),
        ('NVIDIA', 'NVIDIA')
    ]
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES, null=True, blank=True)
    product_image = models.ImageField(default='default.png',upload_to='product_images/')
    date_posted = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def  __str__(self):
        return self.product_name;
    

class Order(models.Model):
    product_ids = models.ManyToManyField(Product)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    STATUS_CHOICES = [
        ('U','Unpaid'),
        ('P', 'Paid'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='U')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_quantity = models.IntegerField(default=0)
    product_quantities = models.JSONField(default=dict)
    
    def __str__(self):
        product_names = ', '.join(str(product) for product in self.product_ids.all())
        return f'Order for: {product_names} by {self.user_id.username}'

   
class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete = models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):  
        return f'{self.product_id.product_name} by {self.user_id.username}';
    
    def total_price(self):
        return self.product_id.price * self.quantity


