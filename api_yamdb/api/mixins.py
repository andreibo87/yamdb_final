from rest_framework import mixins, viewsets


class CustomMixSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Кастомный миксин для Create, List, Delete операций"""
    pass
