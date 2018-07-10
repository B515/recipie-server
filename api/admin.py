from django.contrib import admin

# Register your models here.
from api.models import Recipe, UserInfo, Tag, Comment, File

admin.site.register(UserInfo)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(File)
