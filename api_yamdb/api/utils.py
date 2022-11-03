from secrets import token_hex

from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(email):
    key = token_hex(16)
    send_mail(
        subject='Код подтверждения Yamdb',
        message=(
            'Ваш код подтверждения указан ниже. Отправьте его и'
            ' username на адрес ...api/v1/auth/token/ и мы поможем'
            ' вам войти в систему.\n'
            f'confirmation_code: {key}'
        ),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return key
