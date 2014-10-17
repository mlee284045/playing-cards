from time import sleep
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from cards.models import Player


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def admin_login(self):
        Player.objects.create_superuser('superuser', 'superuser@test.com', 'mypassword')

        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('admin:index')))

        # let's fill out the form with our superuser's username and password
        self.selenium.find_element_by_name('username').send_keys('superuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('mypassword')

        # Submit the form
        password_input.send_keys(Keys.RETURN)

    def create_new_user(self):
        self.selenium.find_elements_by_link_text('Users')[0].click()

        sleep(.5)
        self.selenium.find_elements_by_link_text('Add user')[0].click()

        sleep(.5)
        # Let's click to add a new card

        # Let's fill out the card form
        self.selenium.find_element_by_name('password').send_keys("new-pw")
        self.selenium.find_element_by_name('username').send_keys("new-user")
        self.selenium.find_element_by_name('phone').send_keys("351-111-9876")
        sleep(.5)
        self.selenium.find_element_by_css_selector("input[value='Save']").click()

    def test_user_login(self):
        user = Player.objects.create_user(username='login-user', email='test@test.com', password='user-pw')

        self.selenium.get("{}{}".format(self.live_server_url, reverse('login')))

        self.selenium.find_element_by_id('id_username').send_keys('login-user')
        password = self.selenium.find_element_by_id('id_password')
        password.send_keys('user-pw')
        password.send_keys(Keys.RETURN)

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Your email address is {}'.format(user.email), body.text)

    def test_user_registration(self):

        self.selenium.get("{}{}".format(self.live_server_url, reverse('register')))

        self.selenium.find_element_by_id('id_username').send_keys('register-user')
        self.selenium.find_element_by_id('id_email').send_keys('register@register.com')
        self.selenium.find_element_by_id('id_password1').send_keys('register-pw')
        self.selenium.find_element_by_id('id_password2').send_keys('register-pw')
        self.selenium.find_element_by_css_selector('input[value="Submit"]').click()

        self.assertTrue(Player.objects.get(username='register-user'))

    def test_admin_login(self):
        self.admin_login()

        # sleep for half a second to let the page load
        sleep(.5)

        # We check to see if 'Site administration' is now on the page, this means we logged in successfully
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)
        sleep(.5)

    def test_admin_create_card(self):
        self.admin_login()
        # We can check that our Card model is registered with the admin and we can click on it
        # Get the 2nd one, since the first is the header

        self.selenium.find_elements_by_link_text('Cards')[1].click()

        # Let's click to add a new card
        self.selenium.find_element_by_link_text('Add card').click()
        # print self.selenium.find_element_by_link_text('Add user')

        # Let's fill out the card form
        self.selenium.find_element_by_name('rank').send_keys("ace")
        suit_dropdown = self.selenium.find_element_by_name('suit')
        for option in suit_dropdown.find_elements_by_tag_name('option'):
            if option.text == "heart":
                option.click()
        sleep(.5)
        self.selenium.find_element_by_css_selector("input[value='Save']").click()

        sleep(.5)

        # Check to see we get the card was added success message
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('The card "ace of hearts" was added successfully', body.text)

    def test_admin_create_player(self):
        self.admin_login()

        # We can check that our Card model is registered with the admin and we can click on it
        # Get the 2nd one, since the first is the header
        self.create_new_user()

        # Check to see we get the card was added success message
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('The user "new-user" was added successfully', body.text)

    def test_admin_edit_player(self):
        self.admin_login()
        self.create_new_user()

        # We can check that our Card model is registered with the admin and we can click on it
        # Get the 2nd one, since the first is the header
        self.selenium.find_elements_by_link_text('new-user')[0].click()

        sleep(.5)

        self.selenium.find_element_by_name('first_name').send_keys("new")
        self.selenium.find_element_by_name('last_name').send_keys("user")
        self.selenium.find_element_by_css_selector("input[value='Save']").click()

        sleep(.5)

        # Check to see we get the card was added success message
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('The user "new-user" was changed successfully', body.text)
