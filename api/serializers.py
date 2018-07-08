from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Recipe, UserInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ('friends', 'recipe_collection')

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(UserInfoSerializer, self).to_representation(instance)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['create_by'] = UserInfoSerializer(read_only=True)
        return super(RecipeSerializer, self).to_representation(instance)