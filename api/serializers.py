from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Recipe, UserInfo, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('read_count', 'like_count', 'collect_count')
        depth = 1


class UserInfoSerializer(serializers.ModelSerializer):
    recipe_created = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ('friends', 'recipe_collection')
        depth = 1
