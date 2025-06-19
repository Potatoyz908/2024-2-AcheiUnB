from rest_framework import serializers

from .models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ["id", "subject", "message", "attachment", "from_email", "created_at"]
        read_only_fields = ["id", "created_at"]
