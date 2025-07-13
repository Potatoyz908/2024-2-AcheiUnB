from django import forms
from django.contrib import admin
from django.utils.html import format_html

from users.tasks import send_report_confirmation, send_report_notification

from .models import CHAT_REPORT_CATEGORIES, ITEM_REPORT_CATEGORIES, Report

ALL_REPORT_CATEGORIES = list(set(ITEM_REPORT_CATEGORIES + CHAT_REPORT_CATEGORIES))


class ReportAdminForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(cat, cat) for cat in ALL_REPORT_CATEGORIES]
        self.fields["categories"] = forms.MultipleChoiceField(
            choices=choices,
            widget=forms.CheckboxSelectMultiple,
            required=True,
            label="Categorias",
        )
        if self.data.getlist("categories") and "Outros" in self.data.getlist("categories"):
            self.fields["description"].required = True
            self.fields["description"].widget.attrs[
                "placeholder"
            ] = "Descreva o motivo da denúncia"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    form = ReportAdminForm
    actions = ["mark_as_resolved", "mark_as_ignored"]

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status="resolved")
        self.message_user(request, f"{updated} denúncias marcadas como Resolvida.")

    mark_as_resolved.short_description = "Marcar denúncias como Resolvida"

    def mark_as_ignored(self, request, queryset):
        updated = queryset.update(status="ignored")
        self.message_user(request, f"{updated} denúncias marcadas como Ignorada.")

    mark_as_ignored.short_description = "Marcar denúncias como Ignorada"

    list_display = (
        "id",
        "report_type",
        "status",
        "reporter",
        "reported_user",
        "item",
        "chatRoom",
        "categories_display",
        "attachment_tag",
        "created_at",
    )
    list_filter = (
        "report_type",
        "status",
        "created_at",
    )
    search_fields = (
        "reporter__username",
        "reported_user__username",
        "item__name",
        "chatRoom__id",
        "description",
        "categories",
    )
    readonly_fields = ("created_at", "attachment_tag")
    ordering = ("-created_at",)

    def categories_display(self, obj):
        if isinstance(obj.categories, list):
            return ", ".join(obj.categories)
        if isinstance(obj.categories, str):
            return obj.categories
        return str(obj.categories)

    categories_display.short_description = "Categorias"

    def attachment_tag(self, obj):
        if obj.attachment:
            if (
                str(obj.attachment)
                .lower()
                .endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".gif",
                        ".bmp",
                        ".webp",
                    )
                )
            ):
                return format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" style="max-height:80px;'
                    'max-width:120px;object-fit:contain;"/>'
                    "</a>",
                    obj.attachment.url,
                    obj.attachment.url,
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank">Ver arquivo</a>',
                    obj.attachment.url,
                )
        return "-"

    attachment_tag.short_description = "Anexo"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("reporter", "reported_user", "item", "chatRoom")

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            send_report_notification.delay(obj.id)
            send_report_confirmation.delay(obj.id)
