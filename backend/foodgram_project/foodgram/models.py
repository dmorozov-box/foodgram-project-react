from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


def validate_color(value):
    RegexValidator(
        r'^#([A-Fa-f0-9]{6})$',
        '{} is not a HEX color code'.format(value),
    )(value)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=200)
    color = models.CharField(
        max_length=7,
        validators=[validate_color]
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
    )
    name = models.CharField(unique=True, max_length=200)
    image = models.ImageField()
    text = models.TextField(null=False)
    tags = models.ManyToManyField(
        Tag,
        default=None,
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
        )
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredients",
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        unique_together = ['recipe', 'ingredient']
        ordering = ['ingredient']


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_uc'
            )
        ]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shoppinglist',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shoppinglist',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='shoppinglist_uc'
            )
        ]
