from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import CustomMixSet
from .permissions import (IsRoleAdmin, IsRoleAdminOrReadOnly, IsRoleAuthor,
                          IsRoleModerator, ReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailSerializer, GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)
from .utils import send_confirmation_code


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление модели Title.
    Обрабатывает все запросы с учетом прав доступа.
    Получить список всех произведений - доступно без токена.
    Создать новое произведение - только Администратор.
    Получить конкретное произведение по id - доступно без токена.
    Отредактировать произведение по id - только Админ.
    Удалить произведение по id - только Админ.
    """
    permission_classes = [IsRoleAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitlesFilter

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('title_reviews__score'))

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(CustomMixSet):
    """
    Представление модели Category.
    Обрабатывает запросы GET, POST и DEL с учетом прав доступа.
    Получить список всех категорий - доступно без токена.
    Создать новую категорию- только Админ.
    Удалить категорию - только Админ.
    """
    queryset = Category.objects.all()
    permission_classes = [IsRoleAdminOrReadOnly]
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CustomMixSet):
    """
    Представление модели Genre.
    Обрабатывает запросы GET, POST и DEL с учетом прав доступа.
    Получить список всех жанров - доступно без токена.
    Создать новый жанр - только Админ.
    Удалить жанр - только Админ.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsRoleAdminOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = [
        IsRoleAuthor | ReadOnly | IsRoleAdmin | IsRoleModerator
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.title_reviews.all()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [
        IsRoleAuthor | ReadOnly | IsRoleAdmin | IsRoleModerator
    ]

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   pk=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        return serializer.save(author=self.request.user, review=review)


class SendEmailView(APIView):
    """
    Получить код подтверждения.
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Эндпоит: http://127.0.0.1:8000/api/v1/auth/signup/.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            raise ValidationError(
                'ОШИБКА - ник или мейл уже занят',
            )
        send_confirmation_code(user.email)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendToken(APIView):
    """
    Направление запроса для получения JWT-токена.
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: **Доступно без токена. Эндпоинт: /api/v1/auth/token/.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        refresh = RefreshToken.for_user(user)
        token = {'access': str(refresh.access_token), }
        return Response(token, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    Права доступа: Администратор.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsRoleAdmin]
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'GET':
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(role=self.request.user.role, partial=True)
