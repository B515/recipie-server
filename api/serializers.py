from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Recipe, UserInfo, Tag, Comment, File


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', "first_name", "last_name", "email", "groups", "user_permissions",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('like_count',)


class RecipeSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('read_count', 'like_count', 'collect_count')
        depth = 1


class TagSerializer(serializers.ModelSerializer):
    recipe_set = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('like_count')


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    recipe_created = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ('friends', 'recipe_collection')
        depth = 1


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
