from audioop import reverse
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
from django import forms
from django.utils.timezone import now


class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(
        null=True, blank=True, upload_to="images/")

    author = models.CharField(max_length=13)
    content2 = models.TextField()
    likes = models.ManyToManyField(User, related_name='blog_posts',)

    REQUIRED_FIELDS = ["title", "author"]

    def __str__(self):
        return 'Message from ' + self.title + ' by ' + str(self.author)

    def get_absolute_url(self):
        return reverse('home01')

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email
