from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet, TagsViewSet, IngredientViewSet, IngredientsViewSet,
    RecipesViewSet, RecipeViewSet,
    ShoppingListViewSet, FavoriteViewSet, SubscriptionWithRecipeViewSet,
    shopping_cart
)

router = DefaultRouter()

router.register('tags', TagsViewSet, basename='tags')
router.register(
    r'tags/(?P<tag_id>\d+)', TagViewSet, basename='tags'
)

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register(
    r'ingredients/(?P<ingredient_id>\d+)', IngredientViewSet,
    basename='ingredients'
)

router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingListViewSet,
    basename='shopping_cart'
)

router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite'
)

router.register('recipes', RecipesViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>\d+)', RecipeViewSet,
    basename='recipes'
)

router.register(
    r'users/(?P<author_id>\d+)/subscribe', SubscriptionWithRecipeViewSet,
    basename='subscribe'
)
router.register(
    r'users/subscriptions', SubscriptionWithRecipeViewSet,
    basename='subscriptions'
)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        shopping_cart,
        name='shopping_cart'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
