from django_filters.rest_framework import (
    ModelMultipleChoiceFilter, BooleanFilter, FilterSet
)
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class RecipeFilter(FilterSet):
    # tags = AllValuesMultipleFilter(field_name='tags__slug')
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shoppinglist__user=self.request.user)
        return queryset


class SearchByNameFilter(SearchFilter):
    search_param = 'name'
