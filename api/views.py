from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.models import Recipe, UserInfo, Tag, Comment, File
from .serializers import RecipeSerializer, UserInfoSerializer, TagSerializer, CommentSerializer, FileSerializer


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
        recipe = serializer.save(create_by=UserInfo.objects.get(user=self.request.user.id))
        for tag_id in self.request.data['tag'].split(','):
            tag = Tag.objects.get(id=tag_id)
            recipe.tag.add(tag)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userinfo=UserInfo.objects.get(user=self.request.user.id))


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=UserInfo.objects.get(user=self.request.user.id))


def index(request):
    return HttpResponse("Welcome to Recipie API.")
