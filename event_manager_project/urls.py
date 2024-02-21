from django.contrib import admin
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from events.views import (
    UserCreate,
    EventViewSet,
    custom_api_root,
    register_for_event,
    unregister_from_event,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Event Manager API",
        default_version="v1",
        description="API documentation for Event Manager App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ivan_kucherenko@ukr.net"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)


router = DefaultRouter()
router.register(r"events", EventViewSet)

urlpatterns = [
    path("", custom_api_root, name="api-root"),
    path(
        "events/",
        EventViewSet.as_view({"get": "list", "post": "create"}),
        name="event-list",
    ),
    path(
        "events/<int:pk>/",
        EventViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="event-detail",
    ),
    path("events/<int:pk>/register/", register_for_event, name="event-register"),
    path("events/<int:pk>/unregister/", unregister_from_event, name="event-unregister"),
    path("admin/", admin.site.urls, name="admin"),
    path("register_user/", UserCreate.as_view(), name="register_user"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
