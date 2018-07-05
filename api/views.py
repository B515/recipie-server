from django.http import HttpResponse
from rest_framework import viewsets

from api.models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def index(request):
    return HttpResponse("Welcome to Recipie API.")
