from django.contrib.auth import get_user_model
from django.db import models

from chat.models import ChatRoom
from users.models import Item

User = get_user_model()

ITEM_REPORT_CATEGORIES = [
    "Item ilegal/proibido",
    "Imagem inadequada",
    "Item falso",
    "Spam/golpe",
    "Outros",
]

CHAT_REPORT_CATEGORIES = [
    "Ofensa/Abuso",
    "Spam",
    "Assédio",
    "Golpe",
    "Mensagem inapropriada",
    "Outros",
]

USER_REPORT_CATEGORIES = [
    "Ofensa/Abuso",
    "Assédio",
    "Comportamento suspeito",
    "Mensagens inadequadas",
    "Perfil inapropriado",
    "Imagem inadequada",
    "Informações falsas",
    "Golpe",
    "Spam",
    "Item falso",
    "Item ilegal/proibido",
    "Roubo de identidade",
    "Uso indevido da plataforma",
    "Outros",
]


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ("item", "Item"),
        ("chat", "Chat"),
        ("user", "User"),
    ]
    STATUS_CHOICES = [
        ("open", "Aberta"),
        ("in_review", "Em análise"),
        ("resolved", "Resolvida"),
        ("ignored", "Ignorada"),
    ]

    reporter = models.ForeignKey(User, related_name="reports_made", on_delete=models.CASCADE)
    reported_user = models.ForeignKey(
        User, related_name="reports_received", on_delete=models.CASCADE
    )
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)

    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)
    chatRoom = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.SET_NULL)

    categories = models.CharField(max_length=50)  # Alterado para armazenar uma única categoria
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to="reports/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    def __str__(self):
        return f"Denúncia {self.id} ({self.report_type})"
