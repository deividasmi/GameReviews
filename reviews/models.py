from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game_score = models.IntegerField()
    review_score = models.IntegerField()
    score_count = models.IntegerField()


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('reviews-detail', kwargs={'pk': self.pk})