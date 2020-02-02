from django.test import TestCase
from apps.tvvroot.models import Order

class OrdersTestCase(TestCase):
    def test_orders(self):
        self.assertNotEquals( Order.objects, None)
