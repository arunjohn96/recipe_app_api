from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredients

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """ return recipe return url """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='main course'):
    """ Create and return a sample tag """
    return Tag.objects.create(user=user, name=name)


def sample_ingredients(user, name='cinammon'):
    """ Create and return a sample ingredient """
    return Ingredients.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """ create and return a sample recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ Test unauthenticated recipe access """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ test authentication is required """
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """ Test for authenticted recipe access """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test3@test.com',
            'test@123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """ Test for retieveing a list of recipes """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """ Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass@123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """ test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tag.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredients(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
