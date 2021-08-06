from django.db.models import Q


from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from django.http import JsonResponse

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from home.models import Message

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from .serializers import (
    HomeSerializer
    )



class HomeView(APIView):
    queryset = Message.objects.all()
    serializer_class = HomeSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    http_method_names = ['get', 'head']

    def get(self, request, format=None):
        messages = Message.objects.all()
        serializer = HomeSerializer
        return Response({"message": "UHUL! The API is UP && RUNNING!"})