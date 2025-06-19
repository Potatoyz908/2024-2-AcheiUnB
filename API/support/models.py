from django.conf import settings
from django.db import models


class SupportTicket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="support_tickets",
        null=True,
        blank=True,
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    attachment = models.FileField(upload_to="support_attachments/", null=True, blank=True)
    from_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.from_email}"
