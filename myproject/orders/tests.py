from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cart.models import CartModel
from products.models import CategoryModel, ProductModel

from .models import AddressModel, OrderItem, Orders


class OrderFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='password123')
        self.other_user = User.objects.create_user(
            username='other', password='password123'
        )
        self.category = CategoryModel.objects.create(cname='Test')
        self.product = ProductModel.objects.create(
            category=self.category,
            pname='Test product',
            price=Decimal('10.00'),
            pdesc='Test',
            quantity=3,
        )
        self.address = AddressModel.objects.create(
            user=self.user,
            fullname='Buyer',
            mobile='1234567890',
            address_line='1 Test Street',
            city='Test City',
            state='Test State',
            pincode='123456',
        )

    def test_checkout_creates_order_reduces_stock_and_clears_cart(self):
        self.client.force_login(self.user)
        CartModel.objects.create(
            user=self.user,
            product_c=self.product,
            product_count=2,
            total_price=Decimal('20.00'),
        )

        response = self.client.post(
            reverse('check_out'),
            {'address': self.address.id},
        )

        self.assertRedirects(response, reverse('order_'))
        self.assertEqual(Orders.objects.count(), 1)
        self.assertEqual(OrderItem.objects.get().quantity, 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 1)
        self.assertEqual(CartModel.objects.count(), 0)

    def test_address_update_cannot_access_another_users_address(self):
        foreign_address = AddressModel.objects.create(
            user=self.other_user,
            fullname='Other',
            mobile='1234567890',
            address_line='Other Street',
            city='Other City',
            state='Other State',
            pincode='654321',
        )
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('update_address', args=[foreign_address.id])
        )

        self.assertEqual(response.status_code, 404)

