from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Team(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
BRAND_CHOICES = [
    ('Nike', 'Nike'),
    ('Adidas', 'Adidas'),
    ('Puma', 'Puma'),
    ('Under Armour', 'Under Armour'),
    ('New Balance', 'New Balance'),
    ('Other', 'Other'),
]

TYPE_CHOICES = [
    ('Home', 'Home'),
    ('Away', 'Away'),
    ('Third', 'Third'),
    ('Goalkeeper', 'Goalkeeper'),
    ('Training', 'Training'),
    ('Other', 'Other'),
]

SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
]

class Jersey(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_retro = models.BooleanField(default=False)
    image = models.ImageField(upload_to='jersey_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.team.slug}-{self.size}-{self.type}".lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team.name} {self.get_type_display()} {self.get_size_display()}"
    
    def get_absolute_url(self):
        return reverse('jersey_detail', args=[self.slug])