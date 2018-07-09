from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Recipe, UserInfo, Tag
from .serializers import RecipeSerializer, UserInfoSerializer, TagSerializer


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False)
    def me(self, request):
        me = UserInfo.objects.get(user=request.user.id)
        serializer = self.get_serializer(me)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def update_me(self, request):
        me = UserInfo.objects.get(user=request.user.id)
        serializer = self.get_serializer(me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(create_by=UserInfo.objects.get(user=self.request.user.id))


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def index(request):
    return HttpResponse("Welcome to Recipie API.")
