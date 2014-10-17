from django.test import TestCase
from cards.models import WarGame
from cards.test.factories import WarGameFactory, PlayerFactory


class PlayerModelTestCase(TestCase):
    def setUp(self):
        self.user = PlayerFactory()

    def test_get_wins(self):
        WarGameFactory.create_batch(2, player=self.user, result=WarGame.WIN)
        self.assertEqual(self.user.get_wins(), 2)

    def test_get_losses(self):
        WarGameFactory.create_batch(3, player=self.user, result=WarGame.LOSS)
        self.assertEqual(self.user.get_losses(), 3)

    def test_get_ties(self):
        WarGameFactory.create_batch(4, player=self.user, result=WarGame.TIE)
        self.assertEqual(self.user.get_ties(), 4)

    def test_get_record_display(self):
        WarGameFactory.create_batch(2, player=self.user, result=WarGame.WIN)
        WarGameFactory.create_batch(3, player=self.user, result=WarGame.LOSS)
        WarGameFactory.create_batch(4, player=self.user, result=WarGame.TIE)
        self.assertEqual(self.user.get_record_display(), "2-3-4")

    def test_get_badges(self):
        WarGameFactory.create_batch(3, player=self.user, result=WarGame.WIN)
        self.assertEqual(self.user.get_badges(), 'N00B')
        WarGameFactory.create_batch(6, player=self.user, result=WarGame.WIN)
        self.assertEqual(self.user.get_badges(), 'Beginner Winner')
        WarGameFactory.create_batch(16, player=self.user, result=WarGame.WIN)
        self.assertEqual(self.user.get_badges(), 'Intermediate Collegiate')
        WarGameFactory.create_batch(31, player=self.user, result=WarGame.WIN)
        self.assertEqual(self.user.get_badges(), 'Advanced Stance')
