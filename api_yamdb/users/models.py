from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.validators import username_validation

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)

MAX_LENGTH_ROLE = max(len(role[0]) for role in ROLE_CHOICES)


class User(AbstractUser):
    """
    Модель пользователя.
    Username, email обязательны. Остальные поля опциональны.
    """
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. Letters, '
            'digits and @/./+/-/_ only.'
        ),
        validators=[username_validation],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    first_name = models.CharField('first name', max_length=150, blank=True)
    email = models.EmailField('email address', unique=True)
    bio = models.TextField('biography', blank=True)
    role = models.CharField(
        'user role',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField('confirmation_code', max_length=16)

    class Meta:
        ordering = ('id',)

    @property
    def is_admin(self):
        """True если пользователь Админ."""
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        """True если пользователь Модератор."""
        return (self.role == MODERATOR) or self.is_admin

    def __str__(self):
        return self.username
