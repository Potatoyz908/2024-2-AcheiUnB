import logging

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SupportTicketSerializer

logger = logging.getLogger(__name__)


class ReportProblemView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            # Salvar o ticket no banco de dados
            ticket = serializer.save()

            try:
                # Configurar o email
                subject = f"[ACHEI UNB] Problema Reportado: {ticket.subject}"
                message = f"""
                Um novo problema foi reportado:

                De: {ticket.from_email}
                Assunto: {ticket.subject}

                Mensagem:
                {ticket.message}

                Este email foi enviado automaticamente pelo sistema AcheiUnB.
                """

                email = EmailMessage(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.SUPPORT_EMAIL],
                    reply_to=[ticket.from_email],
                )

                # Adicionar anexo, se houver
                if ticket.attachment:
                    email.attach_file(ticket.attachment.path)

                # Enviar o email
                email.send()

                return Response(
                    {"message": "Problema reportado com sucesso!"},
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                logger.error(f"Erro ao enviar email de suporte: {str(e)}")
                # Mesmo com erro no email, o ticket foi salvo, então retornamos sucesso
                return Response(
                    {"message": "Problema registrado, mas houve um erro ao enviar o email."},
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
