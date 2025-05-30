from rest_framework import serializers

from .models import CHAT_REPORT_CATEGORIES, ITEM_REPORT_CATEGORIES, Report


class ReportSerializer(serializers.ModelSerializer):
    def validate(self, data):
        report_type = data.get("report_type")
        categories = data.get("categories", [])
        if report_type == "item":
            valid_categories = ITEM_REPORT_CATEGORIES
        elif report_type == "chat":
            valid_categories = CHAT_REPORT_CATEGORIES
        else:
            raise serializers.ValidationError({"report_type": "Tipo de denúncia inválido."})

        if not isinstance(categories, list):
            raise serializers.ValidationError(
                {"categories": "Deve ser uma lista de categorias."}
            )
        for cat in categories:
            if cat not in valid_categories:
                raise serializers.ValidationError({"categories": f"Categoria inválida: {cat}"})
        return data

    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ["reporter", "reported_user", "created_at", "status"]
