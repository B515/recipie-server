"""recipie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views
from recipie import settings

router = routers.DefaultRouter()
router.register(r'users', views.UserInfoViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'files', views.FileViewSet)
urlpatterns = [
                  path('', views.index),
                  path('api/', include(router.urls)),
                  path('auth/', include('rest_auth.urls')),
                  path('auth/registration/', include('rest_auth.registration.urls')),
                  path('jet/', include('jet.urls', 'jet')),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
