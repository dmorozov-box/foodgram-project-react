from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    Tag, Ingredient, RecipeIngredient, Recipe,
    ShoppingList, Favorite, Subscription
)

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


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

    favorite.short_description = 'Сколько раз добавили в избранное'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList)
admin.site.register(Favorite)
admin.site.register(Subscription)
