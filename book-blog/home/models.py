from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model):
    genre_choices = (
        ('education','Education'),
        ('movie','Movie'),
        ('sports','Sports'),
        ('other','Other')
    )
    genre = models.CharField(max_length=20,choices=genre_choices,default='education')
    image = models.ImageField(upload_to='blog_images/',blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_text = models.TextField()
    comment_author = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)