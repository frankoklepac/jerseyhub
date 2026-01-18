import os
from django.db import models
from django.contrib.auth.models import User
from jerseys.models import Team

# Create your models here.
BRAND_CHOICES = [
    ('Nike', 'Nike'),
    ('Adidas', 'Adidas'),
    ('Puma', 'Puma'),
    ('Under Armour', 'Under Armour'),
    ('New Balance', 'New Balance'),
    ('Other', 'Other'),
]

SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
]

TYPE_CHOICES = [
    ('Home', 'Home'),
    ('Away', 'Away'),
    ('Third', 'Third'),
    ('Goalkeeper', 'Goalkeeper'),
    ('Training', 'Training'),
    ('Other', 'Other'),
]

def get_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.slug:
        filename = f"{instance.slug}.{ext}"
    else:
        filename = f"{instance.title.replace(' ', '_')}.{ext}"
    return os.path.join('marketplace_images/', filename)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_retro = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.team.slug}-{self.size}-{self.type}-{self.owner.username}-{self.price}".lower().replace(' ', '-')
        super().save(*args, **kwargs)
