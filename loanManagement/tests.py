from django.test import TestCase,Client
#from .models import Loan,Users
import json
from rest_framework import status
from django.urls import reverse
from .serializers import *
from rest_framework.test import APIRequestFactory ,APITestCase
from .models import User,Loan

class TestUserRegister(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
    
        url = reverse('register')
        data = {'email': 'NewUser@user.com','password':'MyPass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'NewUser@user.com')
        self.assertEqual(User.objects.get().role,3)

    def test_create_superuser(self):
        user= User.objects.create_superuser('admin@admin.com', 'pass')
        user=create_superuser('admin@admin.com','pass')
        self.assertEqual(user.count(), 1)
        self.assertEqual(user.email, 'admin@admin.com')
        self.assertEqual(user.role,1)

        


# class TestUserListView(APITestCase):
#     factory = APIRequestFactory()
#     request = factory.post('/notes/', {'title': 'new idea'}, format='json')