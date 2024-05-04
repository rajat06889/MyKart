from django.db import models
from django.urls import reverse
#from django.core.urlresolvers import reverse

class Category(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list_product', args=[self.slug])

class Product(models.Model):
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='unbranded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product_info', args=[self.slug])

