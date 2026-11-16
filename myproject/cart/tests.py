from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import CategoryModel, ProductModel
from .models import CartModel


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='password')
        self.other_user = User.objects.create_user(username='other', password='password')
        category = CategoryModel.objects.create(cname='Books')
        self.product = ProductModel.objects.create(
            category=category,
            pname='Book',
            price=10,
            pdesc='A book',
            quantity=5,
        )

    def test_anonymous_users_are_redirected_to_login(self):
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))

        self.assertRedirects(
            response,
            f"{reverse('login_')}?next={reverse('add_to_cart', args=[self.product.id])}",
        )
        self.assertEqual(CartModel.objects.count(), 0)

    def test_add_to_cart_is_scoped_to_logged_in_user(self):
        self.client.force_login(self.user)
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.client.get(reverse('add_to_cart', args=[self.product.id]))

        cart_item = CartModel.objects.get(user=self.user, product_c=self.product)
        self.assertEqual(cart_item.product_count, 2)
        self.assertEqual(cart_item.total_price, 20)

        CartModel.objects.create(
            user=self.other_user,
            product_c=self.product,
            total_price=10,
        )
        self.client.get(reverse('cart'))
        self.assertEqual(CartModel.objects.filter(user=self.user).count(), 1)
