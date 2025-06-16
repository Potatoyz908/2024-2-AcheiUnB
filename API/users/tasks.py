import os
from datetime import timedelta

import cloudinary.uploader
from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now

from chat.models import Message
from reports.models import Report

from .models import Item, ItemImage, UserProfile


@shared_task
def send_match_notification(to_email, item_name, matches):
    subject = f"Possíveis matches para o seu item perdido: {item_name}"
    html_message = render_to_string(
        "emails/match_notification.html",
        {"item_name": item_name, "matches": matches},
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        "acheiunb2024@gmail.com",
        [to_email],
        html_message=html_message,
    )


@shared_task
def send_welcome_email(user_email, user_name):
    """Task assíncrona para enviar o e-mail de boas-vindas."""
    try:
        # user_name já é tratado no sinal para usar last_name
        # se first_name não estiver disponível
        subject = "Bem-vindo ao AcheiUnB!"
        html_message = render_to_string("emails/welcome.html", {"name": user_name})
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            "acheiunb2024@gmail.com",
            [user_email],
            html_message=html_message,
        )
    except Exception as e:
        print(f"Erro ao enviar o e-mail de boas-vindas: {e}")


@shared_task
def find_and_notify_matches_task(target_item_id, max_distance=2):
    from .match import find_and_notify_matches

    """Task assíncrona para encontrar e notificar matches."""
    try:
        target_item = Item.objects.get(id=target_item_id)
    except Item.DoesNotExist:
        return

    find_and_notify_matches(target_item, max_distance)


@shared_task
def upload_images_to_cloudinary(object_id, images, object_type="item"):
    """Realiza o upload das imagens para o Cloudinary e salva as URLs no banco."""
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )
    try:
        if object_type == "item":
            obj = Item.objects.get(id=object_id)
        elif object_type == "user":
            obj = UserProfile.objects.get(id=object_id)
        else:
            return
    except ObjectDoesNotExist:
        return

    for image_content in images:
        try:
            upload_result = cloudinary.uploader.upload(image_content)
            image_url = upload_result.get("secure_url")

            if object_type == "item":
                ItemImage.objects.create(item=obj, image_url=image_url)

            elif object_type == "user":
                obj.profile_picture = image_url
                obj.save()
        except Exception as e:
            print(f"Erro ao fazer upload de imagem para o objeto {object_id}: {e}")


@shared_task
def remove_images_from_item(image_ids):
    """Remove imagens associadas a um item."""
    try:
        ItemImage.objects.filter(id__in=image_ids).delete()
    except Exception as e:
        print(f"Erro ao remover imagens com IDs {image_ids}: {e}")


@shared_task
def delete_old_items_and_chats():
    """Exclui itens com mais de 2 semanas e os chats vinculados automaticamente."""
    cutoff_date = now() - timedelta(weeks=2)

    old_items = Item.objects.filter(created_at__lt=cutoff_date)

    item_ids = [item.id for item in old_items]
    print(f"Itens encontrados para exclusão: {item_ids}")

    count = old_items.count()
    old_items.delete()

    return f"{count} itens e seus chats vinculados foram excluídos."


@shared_task
def send_ban_notification_email(user_email, first_name, last_name):
    subject = "Notificação de Banimento - AcheiUnB"
    # first_name e last_name já são tratados no sinal
    user_full_name = first_name
    if last_name:
        user_full_name += f" {last_name}"

    message = (
        f"Olá {user_full_name},\n\n"
        "Informamos que sua conta no AcheiUnB foi banida.\n"
        "Se você acredita que isso foi um erro, entre em contato com o suporte."
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [user_email],
        fail_silently=False,
    )

    return f"E-mail de banimento enviado para {user_email}"


@shared_task
def send_unban_notification_email(user_email, first_name, last_name):
    subject = "Sua conta foi desbloqueada - AcheiUnB"
    # first_name e last_name já são tratados no sinal
    user_full_name = first_name
    if last_name:
        user_full_name += f" {last_name}"

    message = (
        f"Olá {user_full_name},\n\n"
        "Informamos que sua conta no AcheiUnB foi desbloqueada.\n"
        "Você já pode voltar a utilizar a plataforma normalmente.\n\n"
        "Se tiver dúvidas, entre em contato com nosso suporte."
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [user_email],
        fail_silently=False,
    )

    return f"E-mail de desbloqueio enviado para {user_email}"


@shared_task
def delete_old_messages(room_id, max_messages=40):
    """
    Mantém apenas as últimas `max_messages` mensagens em uma conversa.
    """
    messages = Message.objects.filter(room_id=room_id).order_by("-timestamp")
    if messages.count() > max_messages:
        ids_to_keep = messages.values_list("id", flat=True)[:max_messages]
        Message.objects.filter(room_id=room_id).exclude(id__in=ids_to_keep).delete()


# --- Notificações de denúncia ---
def build_report_email_body(report):
    body = f"""
Nova denúncia recebida no AcheiUnB:

Tipo: {report.get_report_type_display()}
Status: {report.get_status_display()}
Denunciante: {report.reporter}
Denunciado: {report.reported_user}
Categorias: {', '.join(report.categories) if isinstance(report.categories, list)
             else report.categories}
Descrição: {report.description}
Data/Hora: {report.created_at}
"""
    if report.item:
        body += f"\nItem: {report.item} (ID: {report.item.id})"
    if report.chatRoom:
        body += f"\nChatRoom ID: {report.chatRoom.id}"
    return body


@shared_task
def send_report_notification(report_id):
    try:
        report = Report.objects.get(id=report_id)
        subject = f"Nova denúncia ({report.get_report_type_display()}) no AcheiUnB"
        body = build_report_email_body(report)
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ["acheiunb2024@gmail.com"],
        )
        if report.attachment:
            email.attach_file(report.attachment.path)
        email.send()
    except Exception as e:
        print(f"Erro ao enviar e-mail de notificação de denúncia: {e}")


@shared_task
def send_report_confirmation(report_id):
    try:
        report = Report.objects.get(id=report_id)
        subject = "Recebemos sua denúncia - AcheiUnB"
        body = (
            "Sua denúncia foi recebida e será analisada pela equipe AcheiUnB. "
            "Obrigado por contribuir para a segurança da plataforma!\n\n"
            + build_report_email_body(report)
        )
        reporter_email = getattr(report.reporter, "email", None)
        if not reporter_email:
            print(f"Usuário {report.reporter} não possui e-mail cadastrado.")
            return
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [reporter_email],
        )
        if report.attachment:
            email.attach_file(report.attachment.path)
        email.send()
    except Exception as e:
        print(f"Erro ao enviar e-mail de confirmação de denúncia: {e}")
