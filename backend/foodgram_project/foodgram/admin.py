from django.contrib import admin

from .models import (
    Tag, Ingredient, RecipeIngredient, Recipe,
    ShoppingList, Favorite
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    list_display = ('recipe', 'ingredient', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('favorite',)
    list_display = ('name', 'author',)
    search_fields = ('name', 'author__username', 'tags__name')
    inlines = [RecipeIngredientInline]

    def favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorite.short_description = 'Count in Favorites'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
