from django.test import TestCase
from cards.models import Card
from cards.utils import create_deck


class UtilTestCase(TestCase):
    def test_create_deck(self):
        self.assertEqual(Card.objects.count(), 0)
        create_deck()
        self.assertEqual(Card.objects.count(), 52)
