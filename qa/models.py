from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Question(models.Model):
    title = models.CharField(max_length=1000, unique=True)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id', )


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers')
    content = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        unique_together = ('question', 'user')
        ordering = ('id', )
