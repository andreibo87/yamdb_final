from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from .validators import year_validation

User = get_user_model()

LIM = 15


class Parent(models.Model):
    """Родительский класс-модель для моделей Жанров и Категорий."""
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:LIM]


class Category(Parent):
    """Модель категории, к которой относится произведение."""
    pass


class Genre(Parent):
    """Модель жанра, к которому относится произведение."""
    pass


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(max_length=250)
    year = models.IntegerField(validators=[year_validation])
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        db_table='genre_title'
    )

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name[:LIM]


class Review(models.Model):
    """Модель отзывов на произведение."""

    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_reviews',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]

    def __str__(self):
        return self.text[:LIM]


class Comment(models.Model):
    """Модель  комментариев к отзывам о произведениях."""

    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review_comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date', )

    def __str__(self):
        return self.text[:LIM]
