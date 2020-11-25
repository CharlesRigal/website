from django.test import TestCase
import string
import random
# Create your tests here.

import datetime
from django.utils import timezone
from .models import Post, User

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

'''
class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
'''

class PostModelTests(TestCase):
    def setUp(self):
        # construct list of test user
        for letter in string.ascii_uppercase:
            for number in range(1,10):
                construct_name = "client_"+letter+str(number)
                admin = False
                if number > 9 and letter == 'A': admin = True
                User.objects.create(username=construct_name, is_superuser=admin)

        # add poste
        user_list = User.objects.all()[:20]
        for i, user in zip(range(20), user_list):
            text = "".join([random.choice(string.ascii_lowercase+ " ") for i in range(random.randint(0,2000))])
            Post.objects.create(name="test "+str(i)+" "+user.username, content=text, author=user, date_post=timezone.now())


    def test_none_admin_user_add_post(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.is_superuser, False)
        self.assertRaisesMessage(Post.objects.create(name="bad post",author=user, date_post=timezone.now()),'you no have permition to make this')

    def test_user_likes(self):
        user_list = User.objects.all()
        post = Post.objects.get(pk=2)

        for user in user_list:
            post.likes.add(user)
        
        self.assertEqual(post.total_likes, 234)
        

    def test_user_likes_1_time(self):
        user = User.objects.get(pk=1)
        post = Post.objects.get(pk=1)
        post.likes.add(user)
        self.assertEqual(post.total_likes, 1)

    def test_user_likes_1000_time(self):
        """
        test user like more than can
        """
        post = Post.objects.get(pk=1)
        user = User.objects.get(pk=1)
        for i in range(1000):
            post.likes.add(user)
        self.assertEqual(post.total_likes, 1)
