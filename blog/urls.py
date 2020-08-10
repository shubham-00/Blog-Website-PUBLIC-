from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="blog-home"),
    path("about/", views.about, name="blog-about"),
    path("contact/", views.contact, name="blog-contact"),
    path("feed/", views.feed, name="blog-feed"),
    path("posts/<user>/", views.my_posts, name="blog-my_post"),
    path("post/new/", views.create_post, name="blog-create_post"),
    path("post/delete", views.delete_post, name="blog-delete_post"),
    path("post/<id>/", views.post, name="blog-post"),
    # path('posts/', views.posts, name='blog-posts'),
]
