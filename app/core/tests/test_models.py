from django.test import TestCase
from django.contrib.auth import get_user_model


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
