from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Customer
from .helper.Exceptions import *
import django.db
from django.contrib.auth.models import User



# Create your tests here.
class UserAuthTest(TestCase):
    '''test loging in and registering users'''
    def test_Login(self):
        '''test successful user login'''
        #create test user
        uname = 'test'
        pswd = 'Test12345'
        User = get_user_model()
        User.objects.create_user(username = uname, password = pswd)

        #simulate POST request to login page
        response = self.client.post(reverse('core:login'),{'uname': uname, 'pswd':pswd}, follow = True)

        #check
        self.assertNotEquals(response.context['user'].is_anonymous, True)

    def test_LoginInorrect(self):
        '''test successful user login'''
        #create test user
        uname = 'test'
        pswd = 'Test12345'
        User = get_user_model()
        User.objects.create_user(username = uname, password = pswd)

        #simulate POST request to login page
        response = self.client.post(reverse('core:login'),{'uname': uname, 'pswd':'asdds'}, follow = True)

        #check
        self.assertEquals(response.context['error'], IncorrectUnamePswd)

    def test_LoginEmptyCredential(self):
        '''test failed login attempts due to empty fields'''
        #simulate POST request to login page
        response = self.client.post(reverse('core:login'),{'uname': '', 'pswd':'pswd'}, follow = True)

        #check
        self.assertEquals(response.context['error'], MissingUnamePswd)


    def test_Register(self):
        '''test successful user register'''
        #simulate post request to register page
        response = self.client.post(reverse('core:register'), {
            'uname':'test2', 'pswd':'Test12345', 'email':'obada@hotmail.com', 'phone':65586775}, follow = True)
        
        #check
        self.assertEquals(response.context['user'].is_anonymous, False)

    def test_RegisterShortPass(self):
        '''test unsuccessful registers: short passwords'''
        #simulate post request to register page
        response = self.client.post(reverse("core:register"), {"uname":"test", "pswd":"Test12", 'email':"test@test.com", "phone":123456}, follow=True)

        #check
        self.assertEquals(response.context['error'], PswdLength)

    def test_RegisterEmptyCredential(self):
        '''test unsuccessful registers: empty credientials'''
        #simulate post request to register page
        response = self.client.post(reverse("core:register"), {"uname":"test", "pswd":"", 'email':"test@test.com", "phone":123456}, follow=True)

        #check
        self.assertEquals(response.context['error'], MissingCredentials)

    def test_RegisterExistingRecords(self):
        '''test unsuccessful registers: existing records'''
        #populate db
        User.objects.create_user(username="test", password="Test12345")

        #registering as an existing user
        response = self.client.post(reverse("core:register"), {"uname":"test", "pswd":"Test12345", 'email':"test@test.com", "phone":123456}, follow=True)

        #check
        self.assertEquals(response.context['user'].is_anonymous, True)
        








