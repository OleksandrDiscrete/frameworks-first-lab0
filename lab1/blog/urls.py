from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Система входу/виходу
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Категорії
    path('', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    
    # Статті
    path('articles/', views.article_list, name='article_list'),
    path('article/new/', views.article_create, name='article_create'), # <--- ДОДАНО ЦЕЙ РЯДОК
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # ДОДАНО: Шлях до профілю
    path('profile/', views.profile, name='profile'),
    
    path('', views.category_list, name='category_list'),
    # Коментарі
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]