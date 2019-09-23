from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test.com', password='test@123'):
    """ create a sample User """
    return get_user_model().objects.create_user(email, password)


class Model_Tests(TestCase):
    def test_create_new_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'admin@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalized_email(self):
        """Test for checking the email is in normalized form or not """
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_null_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@123')

    def test_create_super_user(self):
        """ test creating a new super user """
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test@123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ test the ingredient string representation """
        ingredient = models.Ingredients.objects.create(
            user=sample_user(),
            name='cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ Test the recipe string representation """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='puttu',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)
