from django.db import models
from users.models import CustomUser
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.



class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser, related_name='blog_likes', blank=True)
    tags = TaggableManager() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.pk])
    


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name='comment_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog}'

    def total_likes(self):
        return self.likes.count()