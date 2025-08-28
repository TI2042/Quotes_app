from django.db import models
class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.text[:50]} ({self.source})"
