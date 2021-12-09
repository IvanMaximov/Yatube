from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_not_empty

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название группы",
        help_text="Группа, к которой будет относиться пост",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Слаг",
        help_text="Слаг, по которому можно найти группу",
    )
    description = models.TextField(
        verbose_name="Описание группы", help_text="Тематика группы"
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост",
    )
    text = models.TextField(
        validators=[validate_not_empty],
        verbose_name="Текст поста",
        help_text="Текст поста",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата, когда был опубликован пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор поста",
        help_text="Автор поста",
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                       name='unique pair')]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
