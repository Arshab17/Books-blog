from django.shortcuts import render,redirect
from.models import Article,Comment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from.forms import ArticleForm
# Create your views here
@login_required(login_url='signin')
def index(request):

    article=Article.objects.all()
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    if genre:
        article = article.filter(genre__icontains = genre)

    if search:
        article = article.filter(title__icontains=search)
    context = {
        'blogs':article
    }
    return render(request,'index.html',context)
@login_required(login_url='signin')
def article_create(request):
    # if request.user.is_authenticated:
    #     return HttpResponse('your are not authorized ')
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        content = request.POST.get('content')
        Article.objects.create(
            title=title,
            content=content,
            author =request.user,
            genre = genre,
            image = image
        )
        return redirect('home')
    return render(request,'create.html')

def article_details(request,id):
    try:
        article = Article.objects.get(id=id)
    except:
        article = None
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(
            comment_text = comment,
            comment_author = request.user,
            article = article,


        )
    comments = Comment.objects.filter(article=article).order_by('-created')
    context = {
        'article':article,
        'comments':comments
    }
    return render(request,'details.html',context)

def article_edit(request,id):
    try:
        article = Article.objects.get(id=id)
    except:
        article = None
    if request.user != article.author:
        return HttpResponse('you are not authorized to view this page')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article.title = title
        article.content = content
        article.save()
        return redirect('details',article.id)

    context = {
        'article': article
    }
    return render(request,'edit.html',context)

def article_delete(request,id):
    try:
        article = Article.objects.get(id=id)

    except:
        article = None
    if request.user != article.author:
        return HttpResponse('you are not authorized to view this page')
    if request.method =='POST':
        article.delete()
        return redirect('home')
    context = {
        'article': article
    }

    return render(request,'delete.html',context)

def article_new(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
    context = {
        'form' : form
    }
    return render(request,'form.html',context)

def article_edit_new(request,id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST,instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')
        messages.error(request, form.errors)
    context = {
        'article': article
    }
    return render(request,'article_new.html',context)

def comment_delete(request,id):
    comment_dlt = Comment.objects.get(id=id)
    article_id = comment_dlt.article.id
    comment_dlt.delete()
    return redirect('details',article_id)

def comment_edit(request,id):
    edit_comment = Comment.objects.get(id=id)
    article = edit_comment.article
    if request.method == 'POST':
        cmnt = request.POST.get('comment')
        edit_comment.comment_text = cmnt
        edit_comment.save()
        return redirect('details',article.id)

    comments = Comment.objects.filter(article = article)
    context = {
        'edit' : True,
        'edit_comment' : edit_comment,
        'article' : article,
        'comments' : comments
    }
    return render(request,'details.html',context)

