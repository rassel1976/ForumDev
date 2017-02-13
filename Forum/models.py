from django.db import models
from django.contrib.auth.models import User, UserManager

class CustomUser(User):
    """User with app settings."""
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.jpg')
    objects = UserManager()

class Post(models.Model):
    class Meta:
        db_table = "post"
    post_name = models.CharField(max_length=255, verbose_name="Название поста")
    post_text = models.TextField(verbose_name="Текс Поста")
    post_time = models.DateTimeField(auto_now_add=True)
    post_user = models.CharField(max_length=255)

    def __str__(self):
        return self.post_name

class Comment(models.Model):
    class Meta:
        db_table = "comments"
    comment_text = models.TextField(verbose_name="Текст комментария")
    comment_post = models.ForeignKey(Post)
    comment_name = models.CharField(max_length=255)

class Avatar(models.Model):
    class Meta:
        db_table = "avatar"
    avatar = avatar = models.FileField(upload_to='avatars/')
    avatar_user = models.CharField(max_length=255)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FMessage(models.Model):
    fuser = models.CharField(max_length=255)
    suser = models.CharField(max_length=255)
    message = models.TextField(verbose_name="Текс сообщения")

class OMessage(models.Model):
    sm_fm = models.ForeignKey(FMessage)
    user = models.CharField(max_length=255)
    message = models.TextField(verbose_name="Текст сообщения")