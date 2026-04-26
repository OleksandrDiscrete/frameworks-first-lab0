from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Category, Article, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.forms import UserCreationForm

# 1. Список категорій (з кількістю статей)
def category_list(request):
    categories = Category.objects.annotate(articles_count=Count('articles'))
    return render(request, 'blog/category_list.html', {'categories': categories})

# 2. Список статей (з сортуванням)
def article_list(request):
    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'comments':
        articles = Article.objects.annotate(comm_count=Count('comments')).order_by('-comm_count')
    else:
        articles = Article.objects.order_by('-pub_date')
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {'article': article, 'form': form})

# 4. Редагування статті (Авторизація + Ролі)
@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Тільки автор або адміністратор!
    if request.user != article.author and not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user # Автоматично підставляємо поточного користувача
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

# 5. Видалення статті (Авторизація + Ролі)
@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author and not request.user.is_staff:
        raise PermissionDenied
    article.delete()
    return redirect('article_list')

# 6. Видалення коментаря (Авторизація + Ролі)
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_staff:
        raise PermissionDenied
    
    article_pk = comment.article.pk
    comment.delete()
    return redirect('article_detail', pk=article_pk)

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles = category.articles.all().order_by('-pub_date')
    return render(request, 'blog/category_detail.html', {'category': category, 'articles': articles})

@login_required
def profile(request):
    # Якщо профіль ще не існує (для старих користувачів), створюємо його
    Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Зберігаємо користувача (профіль створиться автоматично через сигнал)
            return redirect('login') # Відправляємо на сторінку входу
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})