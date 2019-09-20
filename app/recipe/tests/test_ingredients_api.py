from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredients
from recipe.serializers import IngredientSerializers


INGREDIENTS_URL = reverse('recipe:ingredients-list')


class PublicIngredientsApiTests(TestCase):
    """ Test the publcily availabe ingredients api """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that ingredients is required to access the endpoint """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """ Test that the private ingredients can be
    retrieved by the authorized user """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'test@123'
        )
        self.client.force_authenticate(self.user)

    def test_retreive_ingredients_test(self):
        """ Test for retrieving a list of ingrediensts """
        Ingredients.objects.create(user=self.user, name='salt')
        Ingredients.objects.create(user=self.user, name='SUGAR')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredients.objects.all().order_by('-name')
        serializer = IngredientSerializers(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_for_ingredients_limited_to_user(self):
        """ Test that only ingredients authenticated to users are returned """
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'pass@123'
        )
        Ingredients.objects.create(user=user2, name='Vinegar')

        ingredients = Ingredients.objects.create(user=self.user,
                                                 name='pineapple')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)
