from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Subscription
from .serializers import SubscriptionSerializer


User = get_user_model()


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_author(self):
        author_id = self.kwargs.get('author_id')
        return get_object_or_404(User, id=author_id)

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    def create(self, request, *args, **kwargs):
        author = self.get_author()
        if author == self.request.user:
            return Response(
                'Нельзя подписаться на самого себя.',
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(user=self.request.user, author=author):
            return Response(
                'Вы уже подписаны на автора.',
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, author=self.get_author())

    @action(methods=['delete'], detail=True)
    def delete(self, request, **kwargs):
        object = get_object_or_404(
            Subscription,
            user=self.request.user,
            author=self.get_author()
        )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
