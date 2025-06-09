from rest_framework import serializers

from .models import (
    CHAT_REPORT_CATEGORIES,
    ITEM_REPORT_CATEGORIES,
    USER_REPORT_CATEGORIES,
    Report,
)


class ReportSerializer(serializers.ModelSerializer):
    def validate(self, data):
        report_type = data.get("report_type")
        categories = data.get("categories")  # Alterado para aceitar apenas uma string
        if report_type == "item":
            valid_categories = ITEM_REPORT_CATEGORIES
        elif report_type == "chat":
            valid_categories = CHAT_REPORT_CATEGORIES
        elif report_type == "user":
            valid_categories = USER_REPORT_CATEGORIES
        else:
            raise serializers.ValidationError({"report_type": "Tipo de denúncia inválido."})

        if categories not in valid_categories:
            raise serializers.ValidationError(
                {"categories": f"Categoria inválida: {categories}"}
            )

        # Validações específicas para cada tipo de denúncia
        if report_type == "item" and not data.get("item"):
            raise serializers.ValidationError(
                {"item": "Campo obrigatório para denúncia de item."}
            )
        elif report_type == "chat" and not data.get("chatRoom"):
            raise serializers.ValidationError(
                {"chatRoom": "Campo obrigatório para denúncia de chat."}
            )

        return data

    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ["reporter", "reported_user", "created_at", "status"]
