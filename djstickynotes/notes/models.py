from django.db import models
from django.utils import timezone
from account.models import CustomUser  # Import your custom user model here

class StickyNote(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    last_modified_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
