from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    nickname = models.CharField(max_length=16)
    gender = models.CharField(max_length=16)
    avatar = models.CharField(max_length=1024)
    # 用户关注 多对多联系
    friends = models.ManyToManyField("self", symmetrical=False)
    # 用户-菜谱 多对多关系 (收藏关系)
    recipe_collection = models.ManyToManyField('Recipe')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname


class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=False, default='')
    description = models.CharField(max_length=100, blank=False, default='')
    content = models.TextField(max_length=4096, blank=False, default='')
    read_count = models.IntegerField(default='0')
    like_count = models.IntegerField(default='0')
    collect_count = models.IntegerField(default='0')
    # 用户-菜谱 一对多联系 (属于关系)
    create_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="recipe_created")
    # 菜谱-标签 多对多联系
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)


class Tag(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField(max_length=4096, blank=False, default='')

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=4096, blank=False, default='')
    like_count = models.IntegerField(default='0')
    # 菜谱-评论 一对多联系
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # 用户-评论 一对多联系
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.file
