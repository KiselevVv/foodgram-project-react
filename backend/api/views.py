from rest_framework import status, viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Tag, Ingredient
from .permissions import IsAdminOrReadOnly
from .serializers import CustomUserSerializer, SubscriptionSerializer, \
    TagSerializer, IngredientSerializer

from users.models import User, Subscription


class SubscriptionsListViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.filter(subscribed_to__subscriber=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = CustomUserSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, user_id=None):
        subscriber = request.user
        subscribed_to = get_object_or_404(User, pk=user_id)
        queryset = Subscription.objects.create(
            subscribed_to=subscribed_to,
            subscriber=subscriber
        )
        serializer = SubscriptionSerializer(
            queryset,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id=None):
        subscribed_to = get_object_or_404(User, pk=user_id)
        get_object_or_404(Subscription, subscriber=request.user,
                          subscribed_to=subscribed_to).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None