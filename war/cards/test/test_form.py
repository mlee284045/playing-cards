from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase
from cards.forms import EmailUserCreationForm
from cards.models import Player


class FormTestCase(TestCase):
    def setUp(self):
        # Create a player so that this username we're testing is already taken
        self.player = Player.objects.create_user(username='test-user')
        self.form_same_username = EmailUserCreationForm()
        self.form_diff_username = EmailUserCreationForm()

    def test_clean_username_exception(self):
        # set up the form for testing
        self.form_same_username.cleaned_data = {'username': 'test-user'}
        self.form_diff_username.cleaned_data = {'username': 'mike'}
        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            self.form_same_username.clean_username()
        # asserts clean username is the same as
        self.assertEqual(self.form_diff_username.clean_username(), 'mike')

    def test_register_sends_email(self):
        self.form_diff_username.cleaned_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'test-pw',
            'password2': 'test-pw',
        }
        self.form_diff_username.save()
        # Check there is an email to send
        self.assertEqual(len(mail.outbox), 1)
        # Check the subject is what we expect
        self.assertEqual(mail.outbox[0].subject, 'Welcome!')
