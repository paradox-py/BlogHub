from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('home/blog/<int:pk>/like/', views.like_blog, name='like_blog'),
    path('home/blog/share_blog/', views.email_blog, name='email_blog'),
    path('home/blog/comment/<int:pk>/like/', views.like_comment, name='like_comment'),
]
