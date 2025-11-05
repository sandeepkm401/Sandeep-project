from django.db import models
from django.contrib.auth.models import User

class Finder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=150)
    found_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='finder_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    posted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  
        null=True,
        blank=True,
        related_name="finder_items"
    )

    def __str__(self):
        return f"{self.name} — {self.location}"

class Searcher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    lost_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.location}"



