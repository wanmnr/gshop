# accounts/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import Account

class AccountModelTest(TestCase):
    def setUp(self):
        self.valid_account_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'address': '123 Test St, Test City, TS 12345'
        }

    def test_create_valid_account(self):
        account = Account.objects.create(**self.valid_account_data)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.username, 'testuser')

    def test_username_unique(self):
        Account.objects.create(**self.valid_account_data)
        with self.assertRaises(IntegrityError):
            Account.objects.create(**self.valid_account_data)

    def test_email_unique(self):
        Account.objects.create(**self.valid_account_data)
        new_data = self.valid_account_data.copy()
        new_data['username'] = 'newuser'
        with self.assertRaises(IntegrityError):
            Account.objects.create(**new_data)

    def test_phone_number_validation(self):
        invalid_phone = self.valid_account_data.copy()
        invalid_phone['phone_number'] = 'invalid'
        with self.assertRaises(ValidationError):
            account = Account(**invalid_phone)
            account.full_clean()

    def test_password_hashing(self):
        account = Account.objects.create(**self.valid_account_data)
        self.assertNotEqual(account.password, 'securepassword123')
        self.assertTrue(account.check_password('securepassword123'))

    def test_save_method_updates_timestamp(self):
        account = Account.objects.create(**self.valid_account_data)
        original_updated_at = account.updated_at
        account.first_name = 'Updated'
        account.save()
        self.assertGreater(account.updated_at, original_updated_at)

    def test_empty_fields(self):
        empty_data = {
            'username': '',
            'email': '',
            'password': '',
            'first_name': '',
            'last_name': '',
        }
        with self.assertRaises(ValidationError):
            account = Account(**empty_data)
            account.full_clean()

    def test_invalid_email(self):
        invalid_email = self.valid_account_data.copy()
        invalid_email['email'] = 'invalid_email'
        with self.assertRaises(ValidationError):
            account = Account(**invalid_email)
            account.full_clean()

    def test_username_min_length(self):
        short_username = self.valid_account_data.copy()
        short_username['username'] = 'ab'
        with self.assertRaises(ValidationError):
            account = Account(**short_username)
            account.full_clean()