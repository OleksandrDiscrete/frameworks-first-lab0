from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментар від {self.author.username}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")

    def __str__(self):
        return f'Профіль користувача {self.user.username}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Exception:
        Profile.objects.create(user=instance)