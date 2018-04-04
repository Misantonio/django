from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail
from blog.settings import EMAIL_HOST_USER

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2)
    page_get = request.GET.get('page')
    page = paginator.get_page(page_get)
    try:
        posts = paginator.page(page_get)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'page': page,
                                         'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], cd['comments'])
            message = 'Read "{}" at {}\n\n{}\`s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post,
                                          'form': form,
                                          'sent': sent})
