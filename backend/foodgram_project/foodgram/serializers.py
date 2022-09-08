from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (
    Recipe, Tag, Ingredient, RecipeIngredient,
    Favorite, ShoppingList
)
from users.serializers import UserSerializer, SubscriptionSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient_id',
    )
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True, source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientShortSerializer(RecipeIngredientSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_recipe_in_model(self, obj, model):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return model.objects.filter(user=user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.get_recipe_in_model(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.get_recipe_in_model(obj, ShoppingList)


class RecipeShortSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )


class UserWithRecipeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()

        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit and recipes_limit.isdigit():
            recipes = recipes[:(int(recipes_limit))]

        context = {'request': request}
        return RecipeShortSerializer(recipes, many=True, context=context).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientShortSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time',
        )

    def validate_ingredients_data(self, ingredients):
        if len(ingredients) < 1:
            raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не выбраны.'
                })
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['ingredient_id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться.'
                })
            ingredients_list.append(ingredient_id)
        return ingredients

    def create(self, validated_data):
        ingredients_data = self.validate_ingredients_data(
            validated_data.pop('ingredients')
        )
        tags_data = validated_data.pop('tags')

        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)

        recipe.tags.add(*tags_data)
        for ingredient_data in ingredients_data:
            recipe.ingredients.create(**ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        recipe = get_object_or_404(Recipe, id=instance.id)

        tags_data = validated_data.pop('tags', instance.tags.set)
        recipe.tags.clear()
        recipe.tags.add(*tags_data)

        ingredients_data = self.validate_ingredients_data(
            validated_data.pop('ingredients')
        )
        recipe.ingredients.all().delete()
        for ingredient_data in ingredients_data:
            recipe.ingredients.create(**ingredient_data)

        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data


class ShoppingListSerializer(FavoriteSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')


class IngredientShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')


class SubscriptionWithRecipeSerializer(SubscriptionSerializer):
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return UserWithRecipeSerializer(instance.author, context=context).data
