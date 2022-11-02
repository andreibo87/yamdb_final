import re

from django.utils import timezone
from django.core.exceptions import ValidationError


def year_validation(value):
    """
    Проверка года создания произведения.
    Год создания не может быть больше текущего.
    """
    now = timezone.now().year
    if now < value:
        raise ValidationError(
            f'Год создания не может быть больше чем {now}',
            'Увы, но машину времени еще не изобрели!'
        )


def username_validation(value):
    """Проверка корректности username."""
    if value.lower() == 'me':
        raise ValidationError('me - недопустимое имя')
    if not re.search(r'^[\w.@+-]+$', value):
        message = (
            'В имени пользователя могут быть только буквы, '
            'цифры и знаки @/./+/-/_.'
        )
        raise ValidationError(message)
    return value
