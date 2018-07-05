from django.db import models


class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=False, default='')
    content: models.TextField()
    read_count: models.IntegerField()
    like_count: models.IntegerField()
    collect_count: models.IntegerField()

    class Meta:
        ordering = ('created_at',)
