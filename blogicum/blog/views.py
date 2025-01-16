from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.http import Http404
from blog.models import Post, Category


def index(request):

    posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]

    template = 'blog/index.html'

    context = {'posts': posts}

    return render(request, template, context)


def post_detail(request, pk):

    template = 'blog/detail.html'

    post = get_object_or_404(Post, pk=pk)
    if (
        post.pub_date > now()
        or not post.is_published
        or not post.category.is_published
    ):
        raise Http404("Публикация недоступна.")

    context = {
        "post": post,
    }

    return render(request, template, context)


def category_posts(request, category_slug):

    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована.")

    template = 'blog/category.html'

    posts = (
        Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=now()
        )
        .select_related("author", "location")
        .order_by("-pub_date")
    )

    context = {
        "category": category,
        "posts": posts,
    }

    return render(request, template, context)
