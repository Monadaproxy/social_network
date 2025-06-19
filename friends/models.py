from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    from_user = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = [['from_user', 'to_user']]
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.get_status_display()})"
