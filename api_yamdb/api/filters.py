from django_filters import rest_framework as filters

from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """
    Кастомный класс для фильтрации.
    Тут мы определяем, как фильтровать поля модели.
    """
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = filters.NumberFilter(
        field_name='year',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
