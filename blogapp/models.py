from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout


# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=50)
    content = models.TextField()
    post_slug=models.CharField(max_length=100, blank=True)
    views=models.IntegerField(default=0)
    timestamp=models.DateTimeField(blank=True)

    class Meta:
        ordering = ['-timestamp',]

    def __str__(self):
        return self.title+ ' , ' +self.author

class Blogcomment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField(default=now)

    class Meta:
        ordering = ['-timestamp',]

    def __str__(self):
        return self.comment[0:15]+ "..." + " by "








