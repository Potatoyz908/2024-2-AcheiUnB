from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.tasks import send_report_confirmation, send_report_notification

from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def _validate_duplicate_report(self, reporter, report_type, item, chatRoom):
        if report_type == "item" and item:
            if Report.objects.filter(
                reporter=reporter, report_type="item", item=item
            ).exists():
                raise ValidationError({"item": "Você já enviou uma denúncia para este item."})
        if report_type == "chat" and chatRoom:
            if Report.objects.filter(
                reporter=reporter, report_type="chat", chatRoom=chatRoom
            ).exists():
                raise ValidationError(
                    {"chatRoom": "Você já enviou uma denúncia para este chat."}
                )

    def _get_reported_user(self, report_type, item, chatRoom, reporter):
        if report_type == "item":
            if not item:
                raise ValidationError({"item": "Campo obrigatório para denúncia de item."})
            if not item.user:
                raise ValidationError({"item": "Item sem usuário associado."})
            return item.user
        if report_type == "chat":
            if not chatRoom:
                raise ValidationError({"chatRoom": "Campo obrigatório para denúncia de chat."})
            if chatRoom.participant_1 == reporter:
                return chatRoom.participant_2
            if chatRoom.participant_2 == reporter:
                return chatRoom.participant_1
            raise ValidationError({"chatRoom": "Usuário não faz parte deste chat."})
        raise ValidationError({"report_type": "Tipo de denúncia inválido."})

    def perform_create(self, serializer):
        reporter = self.request.user
        report_type = self.request.data.get("report_type")
        item = serializer.validated_data.get("item")
        chatRoom = serializer.validated_data.get("chatRoom")

        self._validate_duplicate_report(reporter, report_type, item, chatRoom)
        reported_user = self._get_reported_user(report_type, item, chatRoom, reporter)
        instance = serializer.save(reporter=reporter, reported_user=reported_user)

        send_report_notification.delay(instance.id)
        send_report_confirmation.delay(instance.id)
