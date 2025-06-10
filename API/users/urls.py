from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BrandViewSet,
    CategoryViewSet,
    ColorViewSet,
    ItemImageViewSet,
    ItemViewSet,
    LocationViewSet,
    LogoutView,
    MyItemsFoundView,
    MyItemsLostView,
    TestUserView,
    UserDetailView,
    UserListView,
    UserProfileView,
    UserRecentItemsView,
    UserStatsView,
    UserValidateView,
)

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"colors", ColorViewSet, basename="color")
router.register(r"brands", BrandViewSet, basename="brand")
router.register(r"items/(?P<item_id>[^/.]+)/images", ItemImageViewSet, basename="item-image")

urlpatterns = [
    path("items/found/", ItemViewSet.as_view({"get": "list"}), name="found-items"),
    path("items/lost/", ItemViewSet.as_view({"get": "list"}), name="lost-items"),
    path("items/lost/my-items/", MyItemsLostView.as_view(), name="my-lost-items"),
    path("items/found/my-items/", MyItemsFoundView.as_view(), name="my-found-items"),
    path("", include(router.urls)),
    path("auth/validate/", UserValidateView.as_view(), name="user-validate"),
    path("auth/user/", UserDetailView.as_view(), name="user-detail"),
    path("auth/user-profile/<int:user_id>/", UserProfileView.as_view(), name="user-profile"),
    path("auth/user-stats/<int:user_id>/", UserStatsView.as_view(), name="user-stats"),
    path(
        "items/user/<int:user_id>/recent/",
        UserRecentItemsView.as_view(),
        name="user-recent-items",
    ),
    path("test-user/", TestUserView.as_view(), name="test_user"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:user_id>/", UserListView.as_view(), name="user-detail"),
    # Implementação futura sobre matchs path("items/<int:item_id>/matches/",
    # MatchItemViewSet.as_view(), name="item-matches"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
