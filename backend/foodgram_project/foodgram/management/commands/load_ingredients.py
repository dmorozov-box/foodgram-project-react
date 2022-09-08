import json
from django.core.management.base import BaseCommand

from foodgram.models import Ingredient


class Command(BaseCommand):
    help = 'Заполнить model.Ingredient данными из ingredients.json'

    def handle(self, *args, **options):

        with open('ingredients.json', encoding='utf-8') as f:
            ingredients = json.load(f)

        print('LOAD DATA in model.Ingredient ...')
        for ingredient in ingredients:
            if not Ingredient.objects.filter(name=ingredient['name']):
                Ingredient.objects.create(**ingredient)
                print(
                    '[+ Added]: ' + ingredient['name'] + ' - '
                    + ingredient['measurement_unit']
                )
            else:
                print('already exists: ' + ingredient['name'])
