from django.test import TestCase

from users.models import User
from users.services import create_user


class TestUsers(TestCase):
    def test_create_user(self):
        user_count_before = User.objects.count()
        create_user(email="email@hosein-alirezaee.ir", password="1", perform_password_validation=False)

        self.assertEqual(user_count_before, 0)
        self.assertEqual(User.objects.count(), 1)
        user: User = User.objects.get(email="email@hosein-alirezaee.ir")
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("1"))
