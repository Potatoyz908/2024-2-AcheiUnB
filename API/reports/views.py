from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.tasks import send_report_confirmation, send_report_notification

from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def _validate_duplicate_report(self, context):
        """
        Valida se já existe denúncia duplicada.

        Args:
            context: Dicionário contendo reporter, report_type, item, chatRoom e reported_user
        """
        reporter = context.get("reporter")
        report_type = context.get("report_type")
        item = context.get("item")
        chatRoom = context.get("chatRoom")
        reported_user = context.get("reported_user")

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
        if report_type == "user" and reported_user:
            if Report.objects.filter(
                reporter=reporter, report_type="user", reported_user=reported_user
            ).exists():
                raise ValidationError(
                    {"reported_user": "Você já enviou uma denúncia para este usuário."}
                )

    def _get_reported_user(self, context):
        """
        Obtém o usuário que está sendo denunciado.

        Args:
            context: Dicionário contendo report_type, item, chatRoom, reporter e reported_user

        Returns:
            User: O usuário que está sendo denunciado
        """
        report_type = context.get("report_type")
        item = context.get("item")
        chatRoom = context.get("chatRoom")
        reporter = context.get("reporter")
        reported_user = context.get("reported_user")

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
        if report_type == "user":
            if not reported_user:
                raise ValidationError(
                    {"reported_user": "Campo obrigatório para denúncia de usuário."}
                )
            if reported_user == reporter:
                raise ValidationError({"reported_user": "Você não pode denunciar a si mesmo."})
            return reported_user
        raise ValidationError({"report_type": "Tipo de denúncia inválido."})

    def perform_create(self, serializer):
        reporter = self.request.user
        report_type = self.request.data.get("report_type")
        item = serializer.validated_data.get("item")
        chatRoom = serializer.validated_data.get("chatRoom")

        reported_user = None
        if report_type == "user":
            reported_user_id = self.request.data.get("reported_user")
            if not reported_user_id:
                raise ValidationError(
                    {"reported_user": "Campo obrigatório para denúncia de usuário."}
                )
            from django.contrib.auth import get_user_model

            User = get_user_model()
            try:
                reported_user = User.objects.get(id=reported_user_id)
            except User.DoesNotExist:
                raise ValidationError({"reported_user": "Usuário não encontrado."})

        context = {
            "reporter": reporter,
            "report_type": report_type,
            "item": item,
            "chatRoom": chatRoom,
            "reported_user": reported_user,
        }

        self._validate_duplicate_report(context)
        final_reported_user = self._get_reported_user(context)
        instance = serializer.save(reporter=reporter, reported_user=final_reported_user)

        send_report_notification.delay(instance.id)
        send_report_confirmation.delay(instance.id)

    @action(detail=False, methods=["post"], url_path="user")
    def report_user(self, request):
        """
        Endpoint para denúncias de usuários.
        """
        data = request.data.copy()
        data["report_type"] = "user"

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
