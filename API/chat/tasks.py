from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_chat_notification_email(
    recipient_email, recipient_name, item_name, sender_name, chat_url
):
    """
    Envia uma notificação por e-mail quando um novo chat é criado.

    Args:
        recipient_email: E-mail do destinatário
        recipient_name: Nome do destinatário
        item_name: Nome do item relacionado ao chat
        sender_name: Nome do usuário que criou o chat
        chat_url: URL para acessar o chat
    """
    subject = f"AcheiUnB - Novo chat sobre o item: {item_name}"

    # Contexto para o template do e-mail
    context = {
        "recipient_name": recipient_name,
        "sender_name": sender_name,
        "item_name": item_name,
        "chat_url": chat_url,
    }

    # Renderizar o HTML do e-mail
    html_message = render_to_string("emails/chat_notification.html", context)
    plain_message = strip_tags(html_message)

    # Enviar o e-mail
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        html_message=html_message,
        fail_silently=False,
    )

    return f"E-mail de notificação de chat enviado para {recipient_email}"


@shared_task
def mark_messages_as_read(chat_id, user_id, message_id=None):
    """
    Marca todas as mensagens não lidas em um chat como lidas ou uma mensagem específica.

    Args:
        chat_id: ID do chat
        user_id: ID do usuário que está lendo as mensagens
        message_id: ID de uma mensagem específica para marcar como lida (opcional)
    """
    from chat.models import Message

    if message_id:
        # Marcar uma mensagem específica como lida
        try:
            message = Message.objects.get(id=message_id, room_id=chat_id, is_read=False)
            message.is_read = True
            message.save()
            return f"Mensagem {message_id} marcada como lida no chat {chat_id}"
        except Message.DoesNotExist:
            return f"Mensagem {message_id} não encontrada ou já está marcada como lida"
    else:
        # Obtém todas as mensagens não lidas enviadas por outros usuários
        unread_messages = Message.objects.filter(room_id=chat_id, is_read=False).exclude(
            sender_id=user_id
        )

        # Marca as mensagens como lidas
        count = unread_messages.count()
        unread_messages.update(is_read=True)

        return f"Marcadas {count} mensagens como lidas no chat {chat_id}"
