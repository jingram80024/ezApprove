from django.db import models
from PIL import Image
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    # local/unique to each product
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=800)
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    list_price = models.DecimalField(max_digits=6,decimal_places=2)
    sold_price = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    TAG_CHOICES = [
        ('P', 'Pending Approval'),
        ('A', 'Approved'),
        ('S', 'Sold'),
        ('K', 'Kicked Back'),
        ('D', 'Denied'),
    ]
    name = models.CharField(max_length=1,choices=TAG_CHOICES)
    members = models.ManyToManyField(Product, through='TagInfo')

    def __str__(self):
        return self.name

class TagInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now,null=True,blank=True)
    reason_added = models.CharField(max_length=250)

    def __str__(self):
        return self.product.name + " tagged " + self.tag.name