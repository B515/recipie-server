from django.db import models
from django.contrib.auth.models import User


class Userinfo(models.Model):
    nickname = models.CharField(max_length=16)
    gender = models.CharField(max_length=16)
    avatar = models.FileField(upload_to='')
    # 用户关注 多对多联系
    friend = models.ManyToManyField("self", symmetrical=False)
    info = models.ManyToManyField(User)


class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=False, default='')
    content = models.TextField(max_length=4096, blank=False, default='')
    read_count = models.IntegerField(default='0')
    like_count = models.IntegerField(default='0')
    collect_count = models.IntegerField(default='0')
    # 用户-菜谱 一对多联系 (属于关系)
    create_by = models.ForeignKey(Userinfo, on_delete=models.CASCADE, related_name="create")
    # 用户-菜谱 多对多关系 (收藏关系)
    recipe_collection = models.ManyToManyField(Userinfo, through='User_recipe_collection',
                                               through_fields=('recipe_id', 'user_id'))

    class Meta:
        ordering = ('created_at',)


class Tag(models.Model):
    title = models.CharField(max_length=10)
    descrption = models.TextField(max_length=4096, blank=False, default='')
    # 菜谱-标签 多对多联系
    belong = models.ManyToManyField(Recipe, through='Recipe_tag', through_fields=('tag_id', 'recipe_id'))


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=4096, blank=False, default='')
    like_count = models.IntegerField(default='0')
    # 菜谱-评论 一对多联系
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # 用户-评论 一对多联系
    user_id = models.ForeignKey(Userinfo, on_delete=models.CASCADE)


class User_recipe_collection(models.Model):
    user_id = models.ForeignKey(Userinfo, on_delete=models.CASCADE, related_name="collect")
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Recipe_tag(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
