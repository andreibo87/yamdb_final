from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Title, Category, Genre, Comment, Review
from reviews.validators import username_validation
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Только для операций чтения.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Только для операций записи.
    """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        """
        Проверяет не писал ли уже автор POST запроса
        отзыв на это произведение раньше.
        """
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError('Вы уже оставляли свой отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class EmailSerializer(serializers.Serializer):
    """Сериализатор для регистрации и отправки кода на email."""
    email = serializers.EmailField()
    username = serializers.CharField(validators=[username_validation])

    def validate(self, data):
        """Проверка уникальности username и email."""
        if (
            User.objects.filter(email=data['email'])
            .exclude(username=data['username']).exists()
        ):
            raise serializers.ValidationError(
                f'email {data["email"]} уже существует!'
            )
        if (
            User.objects.filter(username=data['username'])
            .exclude(email=data['email']).exists()
        ):
            raise serializers.ValidationError(
                f'username {data["username"]} уже существует!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для работы с токеном JWT."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(User, username=username)
        if data.get('confirmation_code') != user.confirmation_code:
            raise serializers.ValidationError(
                'Некорректный confirmation_code.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью user."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
