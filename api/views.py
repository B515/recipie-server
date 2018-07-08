from django.http import HttpResponse
from rest_framework import viewsets

from api.models import Recipe, UserInfo
from .serializers import RecipeSerializer, UserInfoSerializer


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(create_by=UserInfo.objects.get(user=self.request.user.id))


def index(request):
    return HttpResponse("Welcome to Recipie API.")
