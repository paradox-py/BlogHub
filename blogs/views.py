from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .forms import BlogForm, CommentForm, ShareBlogForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .helpers import share_blog
from django.conf import settings
from taggit.models import Tag
from django.core.exceptions import PermissionDenied

@login_required(login_url='/users/login/')
def home(request):
    try:
        tag = request.GET.get('tag')
        if tag:
            blogs_list = Blog.objects.filter(tags__name__iexact=tag).distinct().order_by('-created_at')
        else:
            blogs_list = Blog.objects.all().order_by('-created_at')

        paginator = Paginator(blogs_list, 5) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        all_tags = Tag.objects.all()  

        return render(request, 'blogs/home.html', {'page_obj': page_obj, 'tag': tag, 'all_tags': all_tags})
    except Exception as e:
        print(f"An error occurred while retrieving the home page: {e}")
        return render(request, 'blogs/home.html', {'error': 'An error occurred. Please try again.'})

@login_required(login_url='/users/login/')
def blog_detail(request, pk):
    try:
        blog = get_object_or_404(Blog, pk=pk)
        comments = blog.comments.all()
        new_comment = None

        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.blog = blog
                new_comment.author = CustomUser.objects.get(pk=request.user.pk) 
                new_comment.save()
                return redirect('blog_detail', pk=blog.pk)
        else:
            comment_form = CommentForm()

        return render(request, 'blogs/blog_detail.html', {
            'blog': blog,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
        })
    except Exception as e:
        print(f"An error occurred while retrieving the blog detail: {e}")
        return render(request, 'blogs/blog_detail.html', {'error': 'An error occurred. Please try again.'})

@login_required(login_url='/users/login/')
@require_POST
def email_blog(request):
    try:
        form = ShareBlogForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            blog_id = form.cleaned_data['blog_id']
            blog = get_object_or_404(Blog, pk=blog_id)
            
            share_blog(
                subject,
                message,
                blog,
                recipient_email,
            )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    except Exception as e:
        print(f"An error occurred while sharing the blog via email: {e}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'}, status=500)

@login_required(login_url='/users/login/')
def like_blog(request, pk):
    try:
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user

        if not isinstance(user, CustomUser):
            user = CustomUser.objects.get(id=user.id)

        if blog.likes.filter(id=user.id).exists():
            blog.likes.remove(user)
            liked = False
        else:
            blog.likes.add(user)
            liked = True

        return JsonResponse({'liked': liked, 'total_likes': blog.total_likes()})
    except Exception as e:
        print(f"An error occurred while liking the blog: {e}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'}, status=500)

@login_required(login_url='/users/login/')
def like_comment(request, pk):
    try:
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user

        if not isinstance(user, CustomUser):
            user = CustomUser.objects.get(id=user.id)

        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return JsonResponse({'liked': liked, 'total_likes': comment.total_likes()})
    except Exception as e:
        print(f"An error occurred while liking the comment: {e}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'}, status=500)
