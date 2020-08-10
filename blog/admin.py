from django.contrib import admin
from .models import Post, Like, Follower

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
