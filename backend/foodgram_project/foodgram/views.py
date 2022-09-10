from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .filters import RecipeFilter, SearchByNameFilter
from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient,
    Favorite, ShoppingList
)
from users.permissions import IsAuthorOrSuperuserOrReadOnlyPermission
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer,  RecipeCreateSerializer, RecipeIngredientSerializer,
    ShoppingListSerializer, FavoriteSerializer,
    SubscriptionWithRecipeSerializer
)
from users.views import SubscriptionViewSet


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        return get_object_or_404(Tag, pk=tag_id)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchByNameFilter,)
    search_fields = ('^name',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        ingredient_id = self.kwargs.get('ingredient_id')
        return get_object_or_404(Ingredient, pk=ingredient_id)


class RecipeIngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = (
        IsAuthorOrSuperuserOrReadOnlyPermission,
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeCreateSerializer
    queryset = Recipe.objects.all()
    permission_classes = (
        IsAuthorOrSuperuserOrReadOnlyPermission,
    )

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        return get_object_or_404(Recipe, pk=recipe_id)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    model = Favorite
    serializer_class = FavoriteSerializer
    queryset = model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_recipe(self):
        recipe_id = self.kwargs.get('recipe_id')
        return get_object_or_404(Recipe, id=recipe_id)

    def create(self, request, *args, **kwargs):
        if self.model.objects.filter(
            user=self.request.user,
            recipe=self.get_recipe()
        ):
            return Response(
                'Рецепт уже добавлен.',
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    @action(methods=['delete'], detail=True)
    def delete(self, request, **kwargs):
        object = get_object_or_404(
            self.model,
            user=self.request.user,
            recipe=self.get_recipe()
        )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListViewSet(FavoriteViewSet):
    model = ShoppingList
    serializer_class = ShoppingListSerializer


class SubscriptionWithRecipeViewSet(SubscriptionViewSet):
    serializer_class = SubscriptionWithRecipeSerializer


def get_shopping_cart_report_content(ingredients):
    header = 'Список покупок.\n\n'
    details = '\n'.join([
        f'{ingredient["name"]} ({ingredient["measurement_unit"]}) - '
        f'{ingredient["amount"]}'
        for ingredient in ingredients
    ])
    return header + details


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def shopping_cart(request):
    user = request.user
    ingredients = Ingredient.objects.filter(
        ingredients__recipe__shoppinglist__user=user
    ).values(
        'name', 'measurement_unit'
    ).annotate(
        amount=Sum('ingredients__amount')
    )

    response = HttpResponse(
        get_shopping_cart_report_content(ingredients),
        'Content-Type: text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename=Cart.txt'
    return response
