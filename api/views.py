from django.db.models import Q
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.models import Recipe, UserInfo, Tag, Comment, File
from .serializers import RecipeSerializer, UserInfoSerializer, TagSerializer, CommentSerializer, FileSerializer


def me(request):
    return UserInfo.objects.get(user=request.user.id)


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(me(request))
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def update_me(self, request):
        serializer = self.get_serializer(me(request), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def follow(self, request, pk=None):
        me(request).friends.add(self.get_object())
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def unfollow(self, request, pk=None):
        me(request).friends.remove(self.get_object())
        return Response({'success': True})

    @action(methods=['get'], detail=False)
    def my_followers(self, request):
        return self.users_response(me(request).userinfo_set)

    @action(methods=['get'], detail=False)
    def my_following(self, request):
        return self.users_response(me(request).friends.all())

    @action(methods=['get'], detail=True)
    def followers(self, request, pk=None):
        return self.users_response(self.get_object().userinfo_set)

    def users_response(self, users):
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        recipe = serializer.save(create_by=me(self.request))
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
        return self.update_collection(request, 'add')

    @action(methods=['post'], detail=True)
    def uncollect(self, request, pk=None):
        return self.update_collection(request, 'remove')

    def update_collection(self, request, action):
        r = self.get_object()
        getattr(me(request).recipe_collection, action)(r)
        r.collect_count = r.recipe_collection.count()
        r.save()
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        return self.update_like(request, 'add')

    @action(methods=['post'], detail=True)
    def unlike(self, request, pk=None):
        return self.update_like(request, 'remove')

    def update_like(self, request, action):
        r = self.get_object()
        getattr(me(request).recipe_like, action)(r)
        r.like_count = r.recipe_like.count()
        r.save()
        return Response({'success': True})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userinfo=me(self.request), recipe=Recipe.objects.get(id=self.request.data['recipe']))

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        return self.update_like(request, 'add')

    @action(methods=['post'], detail=True)
    def unlike(self, request, pk=None):
        return self.update_like(request, 'remove')

    def update_like(self, request, action):
        c = self.get_object()
        getattr(me(request).comment_like, action)(c)
        c.like_count = c.comment_like.count()
        c.save()
        return Response({'success': True})


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=me(self.request))


def index(request):
    return HttpResponse("Welcome to Recipie API.")
