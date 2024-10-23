# accounts/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from ..views import AccountViewSet, AccountSearchView

class TestUrls(APITestCase):
    def test_account_list_url_resolves(self):
        """Test that the account list URL resolves correctly"""
        url = reverse('account-list')
        resolver = resolve(url)
        self.assertEqual(
            resolver.func.cls,
            AccountViewSet,
            "Account list URL should resolve to AccountViewSet"
        )

    def test_account_detail_url_resolves(self):
        """Test that the account detail URL resolves correctly"""
        url = reverse('account-detail', kwargs={'pk': 1})
        resolver = resolve(url)
        self.assertEqual(
            resolver.func.cls,
            AccountViewSet,
            "Account detail URL should resolve to AccountViewSet"
        )

    def test_account_search_url_resolves(self):
        """Test that the account search URL resolves correctly"""
        url = reverse('account-search')
        resolver = resolve(url)
        self.assertEqual(
            resolver.func.view_class,
            AccountSearchView,
            "Account search URL should resolve to AccountSearchView"
        )

    def test_account_change_password_url_resolves(self):
        """Test that the change password URL resolves correctly"""
        url = reverse('account-change-password', kwargs={'pk': 1})
        resolver = resolve(url)
        self.assertEqual(
            resolver.func.cls,
            AccountViewSet,
            "Change password URL should resolve to AccountViewSet"
        )

    def test_url_names_and_patterns(self):
        """Test that all URL patterns are generated correctly"""
        # Test list URL
        self.assertEqual(
            reverse('account-list'),
            '/accounts/',
            "Account list URL pattern is incorrect"
        )

        # Test detail URL
        self.assertEqual(
            reverse('account-detail', kwargs={'pk': 1}),
            '/accounts/1/',
            "Account detail URL pattern is incorrect"
        )

        # Test search URL
        self.assertEqual(
            reverse('account-search'),
            '/accounts/search/',
            "Account search URL pattern is incorrect"
        )

        # Test change password URL
        self.assertEqual(
            reverse('account-change-password', kwargs={'pk': 1}),
            '/accounts/1/change_password/',
            "Change password URL pattern is incorrect"
        )

    def test_invalid_pk_format(self):
        """Test that invalid pk formats raise NoReverseMatch"""
        from django.urls.exceptions import NoReverseMatch
        
        with self.assertRaises(NoReverseMatch):
            reverse('account-detail', kwargs={'pk': 'invalid'})

    def test_viewset_action_urls(self):
        """Test that all viewset actions have correct URLs"""
        # Test create URL (POST to list endpoint)
        self.assertEqual(
            reverse('account-list'),
            '/accounts/',
            "Account create URL pattern is incorrect"
        )

        # Test update URL (PUT to detail endpoint)
        self.assertEqual(
            reverse('account-detail', kwargs={'pk': 1}),
            '/accounts/1/',
            "Account update URL pattern is incorrect"
        )

        # Test partial update URL (PATCH to detail endpoint)
        self.assertEqual(
            reverse('account-detail', kwargs={'pk': 1}),
            '/accounts/1/',
            "Account partial update URL pattern is incorrect"
        )

        # Test delete URL (DELETE to detail endpoint)
        self.assertEqual(
            reverse('account-detail', kwargs={'pk': 1}),
            '/accounts/1/',
            "Account delete URL pattern is incorrect"
        )