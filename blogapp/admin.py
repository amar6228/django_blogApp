from django.contrib import admin
from blogapp.models import Post,Blogcomment

# Register your models here.
admin.site.register((Post, Blogcomment))

