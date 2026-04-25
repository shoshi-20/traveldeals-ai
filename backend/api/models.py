from django.db import models
import uuid
import secrets
from pgvector.django import VectorField


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=64, unique=True, db_index=True)
    brand_color = models.CharField(max_length=7, default="#1E3A5F")  # hex color
    logo_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_urlsafe(40)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Deal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="deals"
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    destination = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    is_embedded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # category: flight / hotel / attraction
    # budget_tier: luxury / mid-range / budget
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.merchant.name})"


class UserQuery(models.Model):
    """Logs every search query for analytics."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    query_text = models.TextField()
    query_embedding = VectorField(dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
