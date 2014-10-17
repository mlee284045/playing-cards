from django.test import TestCase
from cards.models import Card


class WarTestCase(TestCase):
    def setUp(self):
        self.my_card = Card.objects.create(suit=Card.CLUB, rank="ace")
        self.same_card = Card.objects.create(suit=Card.HEART, rank='ace')
        self.comp_card = Card.objects.create(suit=Card.CLUB, rank='jack')

    def test_get_war_result(self):
        self.assertEqual(self.my_card.get_war_result(self.comp_card), 1)
        self.assertEqual(self.comp_card.get_war_result(self.my_card), -1)
        self.assertEqual(self.my_card.get_war_result(self.same_card), 0)
