from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views
from users.views import DeleteUserView, microsoft_callback

schema_view = get_schema_view(
    openapi.Info(
        title="AcheiUnB API",
        default_version="v1",
        description="Documentação interativa das APIs do AcheiUnB",
        terms_of_service="https://www.unb.br",
        contact=openapi.Contact(email="acheiunb2024@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def vue_app(request):
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("microsoft/login/", views.microsoft_login, name="microsoft_login"),
    path("microsoft/callback/", views.microsoft_callback, name="microsoft_callback"),
    path(
        "accounts/microsoft/login/callback/",
        microsoft_callback,
        name="microsoft_callback",
    ),
    path("", vue_app, name="vue_home"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/chat/", include("chat.urls")),
    path("api/", include("users.urls")),
    path("api/", include("reports.urls")),
    path("delete-user/<int:user_id>/", DeleteUserView.as_view(), name="delete_user"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
