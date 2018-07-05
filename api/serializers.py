from rest_framework import serializers

from api.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('pk', 'title', 'content', 'read_count', 'like_count', 'collect_count')
