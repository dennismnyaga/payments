from django.db import models
import uuid

# Create your models here.
class Buyers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    email = models.EmailField()


class CodeRepository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    code_emage = models.ImageField()
    github_url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserCodeAccess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID
    user = models.ForeignKey(Buyers, on_delete=models.CASCADE)
    repository = models.ForeignKey(CodeRepository, on_delete=models.CASCADE)
    access_granted_at = models.DateTimeField(auto_now_add=True)
    is_invitation_sent = models.BooleanField(default=False)
