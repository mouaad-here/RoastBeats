from django.db import models
import uuid

class Roast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    profile_image_url = models.URLField(max_length=500)
    headline = models.CharField(max_length=100)
    score = models.IntegerField()
    roast_body = models.TextField()
    dating_life = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Roast for {self.username} ({self.score}/100)"
