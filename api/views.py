from django.db.models import Q
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

    @action(methods=['post'], detail=True)
    def follow(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.friends.add(self.get_object())
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def unfollow(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.friends.remove(self.get_object())
        return Response({'success': True})

    @action(methods=['get'], detail=False)
    def followers(self, request):
        me = UserInfo.objects.get(user=request.user.id)
        serializer = self.get_serializer(me.userinfo_set, many=True)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        recipe = serializer.save(create_by=UserInfo.objects.get(user=self.request.user.id))
        for tag_id in self.request.data['tag'].split(','):
            tag = Tag.objects.get(id=tag_id)
            recipe.tag.add(tag)

    def retrieve(self, request, *args, **kwargs):
        r = self.get_object()
        r.read_count += 1
        r.save()
        return super(RecipeViewSet, self).retrieve(request, args, kwargs)

    @action(methods=['get'], detail=False)
    def search_by_keyword(self, request):
        keyword = request.query_params['keyword']
        r = Recipe.objects.filter(Q(title__contains=keyword) | Q(description__contains=keyword))
        serializer = RecipeSerializer(r, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def collect(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.recipe_collection.add(self.get_object())
        self.update_collect_count()
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def uncollect(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.recipe_collection.remove(self.get_object())
        self.update_collect_count()
        return Response({'success': True})

    def update_collect_count(self):
        r = self.get_object()
        r.collect_count = r.recipe_collection.count()
        r.save()

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.recipe_like.add(self.get_object())
        self.update_like_count()
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def unlike(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.recipe_like.remove(self.get_object())
        self.update_like_count()
        return Response({'success': True})

    def update_like_count(self):
        r = self.get_object()
        r.like_count = r.recipe_like.count()
        r.save()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userinfo=UserInfo.objects.get(user=self.request.user.id))

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.comment_like.add(self.get_object())
        self.update_like_count()
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def unlike(self, request, pk=None):
        me = UserInfo.objects.get(user=request.user.id)
        me.comment_like.remove(self.get_object())
        self.update_like_count()
        return Response({'success': True})

    def update_like_count(self):
        r = self.get_object()
        r.like_count = r.comment_like.count()
        r.save()


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=UserInfo.objects.get(user=self.request.user.id))


def index(request):
    return HttpResponse("Welcome to Recipie API.")
