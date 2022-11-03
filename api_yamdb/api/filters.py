# from django_filters import rest_framework as filters
import django_filters
from reviews.models import Title


class TitlesFilter(django_filters.rest_framework.FilterSet):
    """
    Кастомный класс для фильтрации.
    Тут мы определяем, как фильтровать поля модели.
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
