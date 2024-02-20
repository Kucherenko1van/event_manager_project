from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets

from .models import Event
from .filters import EventFilter
from .serializers import EventSerializer, UserSerializer


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


@api_view(["GET"])
def custom_api_root(request, format=None):
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
            "register": {
                "url": reverse("register", request=request, format=format),
                "methods": ["POST"],
                "description": "Register a new user. POST required user information.",
            },
        }
    )
