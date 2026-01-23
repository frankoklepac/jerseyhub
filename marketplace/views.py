from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from marketplace.models import Post
from marketplace.forms import PostForm

# Create your views here.
@login_required
def marketplace_home(request):
    posts = Post.objects.filter(is_sold=False)
    
    return render(request, 'marketplace/home.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'marketplace/post_detail.html', {'post': post})

@login_required
def user_posts(request, owner_id):
    posts = Post.objects.filter(owner_id=owner_id)
    return render(request, 'marketplace/user_posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('marketplace_home')
    else:
        form = PostForm()

    return render(request, 'marketplace/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('marketplace_home')
    else:
        form = PostForm(instance=post)

    return render(request, 'marketplace/edit_post.html', {'form': form, 'post': post})

@login_required
def buy_jersey(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.is_sold:
        return render(request, 'marketplace/post_detail.html', {'post': post, 'error': 'This jersey has already been sold.'})
    post.buyer = request.user
    post.is_sold = True
    post.save()

    return redirect('marketplace_home')