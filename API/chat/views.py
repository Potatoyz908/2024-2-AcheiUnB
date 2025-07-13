from django.db import models
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from chat.models import ChatRoom, Message
from users.models import Item
from users.pagination import ChatPagination
from users.tasks import delete_old_messages

from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def unread_messages(self, request):
        """
        Retorna a contagem de mensagens não lidas para o usuário atual.
        """
        user = request.user

        # Buscar todos os chats do usuário
        user_chatrooms = ChatRoom.objects.filter(
            models.Q(participant_1=user) | models.Q(participant_2=user)
        )

        # Contar mensagens não lidas (enviadas por outros usuários)
        unread_count = (
            Message.objects.filter(room__in=user_chatrooms, is_read=False)
            .exclude(sender=user)
            .count()
        )

        return Response({"unread_count": unread_count})

    @swagger_auto_schema(
        operation_description="Cria uma nova sala de chat entre dois usuários "
        + "para um item específico.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "participant_2": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID do segundo participante."
                ),
                "item_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID do item associado à conversa.",
                ),
            },
            required=["participant_2", "item_id"],
        ),
        responses={
            201: openapi.Response("Sala de chat criada", ChatRoomSerializer),
            400: "Erro de validação",
        },
    )
    def create(self, request, *args, **kwargs):
        participant_1_id = request.user.id
        participant_2_id = request.data.get("participant_2")
        item_id = request.data.get("item_id")

        if not participant_2_id or not item_id:
            raise ValidationError("Os campos participant_2 e item são obrigatórios.")

        if participant_1_id == int(participant_2_id):
            raise ValidationError("Não é possível criar um chat consigo mesmo.")

        if not Item.objects.filter(id=item_id).exists():
            raise ValidationError("O item associado não foi encontrado.")

        existing_chat = ChatRoom.objects.filter(
            participant_1=participant_1_id,
            participant_2=participant_2_id,
            item_id=item_id,
        ).first()

        if existing_chat:
            return Response(self.get_serializer(existing_chat).data)

        # Criação do chat
        response = super().create(request, *args, **kwargs)

        # Enviar e-mail de notificação
        from django.contrib.auth.models import User

        from .tasks import send_chat_notification_email

        # Obter dados para o e-mail
        chatroom_id = response.data["id"]
        sender = request.user
        recipient = User.objects.get(id=participant_2_id)
        item = Item.objects.get(id=item_id)

        sender_name = sender.first_name or sender.last_name or sender.username
        recipient_name = recipient.first_name or recipient.last_name or recipient.username
        chat_url = f"https://acheiunb.com.br/#/chat/{chatroom_id}?userId={participant_2_id}&itemId={item_id}"

        # Enviar e-mail de notificação de forma assíncrona
        send_chat_notification_email.delay(
            recipient.email, recipient_name, item.name, sender_name, chat_url
        )

        return response


class MessageViewSet(ModelViewSet):
    """ViewSet para gerenciar mensagens."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination

    @action(detail=False, methods=["post"])
    def mark_as_read(self, request):
        """
        Marca todas as mensagens não lidas em um chat como lidas ou uma mensagem específica.
        """
        chat_id = request.data.get("chat_id")
        message_id = request.data.get("message_id")
        user = request.user

        if not chat_id:
            return Response({"error": "O ID do chat é obrigatório"}, status=400)

        # Verificar se o usuário pertence ao chat
        try:
            filter_condition = models.Q(participant_1=user) | models.Q(participant_2=user)
            ChatRoom.objects.filter(filter_condition, id=chat_id).get()
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat não encontrado ou acesso negado"}, status=404)

        # Marcar mensagens como lidas - seja uma específica ou todas
        from .tasks import mark_messages_as_read

        mark_messages_as_read.delay(chat_id, user.id, message_id)

        # Em ambiente de produção, pegaria o resultado do Celery
        # Aqui vamos executar síncrono para testes e retornar a informação imediata
        marked_messages = []
        if message_id:
            marked_messages = [message_id]

            # Para testes locais, podemos retornar o ID da mensagem
            return Response(
                {
                    "message": "Mensagem específica marcada como lida",
                    "message_ids": marked_messages,
                },
                status=200,
            )
        else:
            # Pegando IDs das mensagens marcadas como lidas
            messages = Message.objects.filter(room_id=chat_id, is_read=False).exclude(
                sender_id=user.id
            )
            marked_messages = list(messages.values_list("id", flat=True))

            return Response(
                {
                    "message": "Todas as mensagens serão marcadas como lidas",
                    "message_ids": marked_messages,
                },
                status=200,
            )

    @swagger_auto_schema(
        operation_description="Lista todas as mensagens de uma sala de chat específica.",
        manual_parameters=[
            openapi.Parameter(
                "room",
                openapi.IN_QUERY,
                description="ID da sala de chat",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: openapi.Response("Lista de mensagens", MessageSerializer(many=True))},
    )
    def get_queryset(self):
        room_id = self.request.query_params.get("room")
        if room_id:
            return Message.objects.filter(room_id=room_id).order_by("timestamp")
        return super().get_queryset().order_by("timestamp")

    @swagger_auto_schema(
        operation_description="Envia uma nova mensagem em uma sala de chat.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "room": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID da sala de chat"
                ),
                "content": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Conteúdo da mensagem"
                ),
            },
            required=["room", "content"],
        ),
        responses={201: openapi.Response("Mensagem enviada", MessageSerializer)},
    )
    def perform_create(self, serializer):
        # Salva a mensagem
        message = serializer.save(sender=self.request.user)

        # Agenda a limpeza de mensagens antigas
        delete_old_messages.delay(message.room_id)


class ClearChatsView(APIView):
    """Endpoint para limpar todas as mensagens e/ou salas de chat."""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Deleta todas as mensagens e salas de chat do sistema.",
        responses={200: "Todos os chats foram limpos com sucesso."},
    )
    def delete(self, request, *args, **kwargs):
        Message.objects.all().delete()
        ChatRoom.objects.all().delete()
        return Response({"detail": "Todos os chats foram limpos com sucesso."})
