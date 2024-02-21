from rest_framework import status
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Event
from .filters import EventFilter
from .serializers import EventSerializer, UserSerializer

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission so that only object owners can edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class UserCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.attendees.add(request.user)
    return Response({"message": "You have successfully registered for the event."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unregister_from_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.attendees.remove(request.user)
    return Response({"message": "You have successfully unregistered from the event."})


@api_view(["GET"])
def custom_api_root(request, format=None):
    base_url = request.build_absolute_uri("/")[:-1]
    return Response(
        {
            "swagger-ui": {
                "url": request.build_absolute_uri("/swagger/"),
                "methods": ["GET"],
                "description": "Interactive Swagger documentation.",
            },
            "events": {
                "url": reverse("event-list", request=request, format=format),
                "methods": ["GET", "POST"],
                "description": "Retrieve, create events. POST to create an event.",
            },
            "admin": {
                "url": request.build_absolute_uri("/admin/"),
                "methods": ["GET"],
                "description": "Django admin interface.",
            },
            "token_obtain_pair": {
                "url": request.build_absolute_uri("api/token/"),
                "methods": ["POST"],
                "description": "Obtain JWT token pair. POST your username and password.",
            },
            "token_refresh": {
                "url": request.build_absolute_uri("api/token/refresh/"),
                "methods": ["POST"],
                "description": "Refresh JWT access token using a refresh token.",
            },
            "register_user": {
                "url": reverse("register_user", request=request, format=format),
                "methods": ["POST"],
                "description": "Register a new user. POST required user information.",
            },
            "event-register": {
                "url": f"{base_url}/events/{{pk}}/register/",
                "methods": ["POST"],
                "description": "Register for an event. Replace {pk} with event ID.",
            },
            "event-unregister": {
                "url": f"{base_url}/events/{{pk}}/unregister/",
                "methods": ["POST"],
                "description": "Unregister from an event. Replace {pk} with event ID.",
            },
        }
    )
