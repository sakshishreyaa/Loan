from django.test import TestCase,Client
#from .models import Loan,Users
import json
from rest_framework import status
from django.urls import reverse,include,path
from .serializers import *
from rest_framework.test import APIRequestFactory ,APITestCase, URLPatternsTestCase
from .models import User,Loan
from datetime import date
        
class LoanApiTestCase(APITestCase, URLPatternsTestCase):
    """ Test module for Loan Manageent api """

    urlpatterns = [
        path('loanManagement/', include('loanManagement.urls')),
    ]

    def setUp(self):
        self.customer2 = User.objects.create_user(
            email='custii@test.com',
            password='custii',
            id=4
        )
        self.customer = User.objects.create_user(
            email='cust@test.com',
            password='cust',
            id=3
        )
        self.agent = User.objects.create_user(
            email='agent@test.com',
            password='agent',
            role=2,
            id=2
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin',
            id=1
        )

        self.loan=Loan.objects.create(
            customerId=self.customer,
            agentId=self.agent,
            loan_amount=10000,
            tenure=12,
            interest=6.5,
            asset_value=50000
        )
        self.loan2=Loan.objects.create(
            customerId=self.customer,
            agentId=self.agent,
            loan_amount=10000,
            tenure=10,
            interest=7.5,
            asset_value=50000,
            state='Approved',

        )
        self.loan3=Loan.objects.create(
            customerId=self.customer2,
            agentId=self.agent,
            loan_amount=10000,
            tenure=10,
            interest=7.5,
            asset_value=50000,
        
        )
        
    def token_setup(self,email,password):
        url = reverse('login')
        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        return response,response_data

    def test_login(self):
        """ Test if a user can login and get a JWT response token """
        url = reverse('login')
        data = {
            'email': 'admin@test.com',
            'password': 'admin'
        }
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['success'], True)
        self.assertTrue('access' in response_data)
        

    def test_user_registration(self):
        """ Test if a user can register """
        url = reverse('register')
        data = {
            'email': 'test2@test.com',
            'password': 'test',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_UserListView(self):
        """ Test fetching all users for ADMIN"""
        # Setup the token 
        response,response_data=self.token_setup('admin@test.com','admin')
        token = response_data['access']

        # Test the endpoint
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('userlist'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), len(response_data['users']))

        """ Test fetching all users for AGENT """
        # Setup the token
        response,response_data=self.token_setup('agent@test.com','agent')
        token = response_data['access']

        # Test the endpoint
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('userlist'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), len(response_data['users']))
    

        """ Test fetching all users for CUSTOMERS """
        # Setup the token
        response,response_data=self.token_setup('cust@test.com','cust')
        token = response_data['access']

        # Test the endpoint
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('userlist'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response_data['success'])

    def test_UserDetailView(self):
        """ Test fetching and editing any user for ADMIN"""
        # Setup the token 
        response,response_data=self.token_setup('admin@test.com','admin')
        token = response_data['access']

        # Test admin can view any user's details 
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('userdetail',args=(1,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response =self.client.get(reverse('userdetail',args=(2,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response =self.client.get(reverse('userdetail',args=(2,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        #Test admin can edit any user's details
        response =self.client.patch(reverse('userdetail',args=(3,)),data={'first_name':'myname'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'],'User details successfully updated!')

        response =self.client.patch(reverse('userdetail',args=(2,)),data={'first_name':'newname'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'],'User details successfully updated!')

        response =self.client.patch(reverse('userdetail',args=(2,)),data={'first_name':'mynewname'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'],'User details successfully updated!')

        """ Test fetching and editing any user for AGENT """
        # Setup the token
        response,response_data=self.token_setup('agent@test.com','agent')
        token = response_data['access']

        # Test agent can view any user's details
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('userdetail',args=(1,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Test agent canedit any users details
        response =self.client.patch(reverse('userdetail',args=(3,)),data={'first_name':'myname'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'],'User details successfully updated!')

        response =self.client.patch(reverse('userdetail',args=(2,)),data={'first_name':'myname'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['message'],'User details successfully updated!')
    

        """ Test fetching and editing only their own name and email for CUSTOMERS """
        # Setup the token
        response,response_data=self.token_setup('cust@test.com','cust')
        token = response_data['access']

        # Test customer can not get anyone else's user details
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('userdetail',args=(1,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response_data['success'])
        
        # Test customer can not edit anyone else's user details
        response =self.client.patch(reverse('userdetail',args=(2,)),data={'first_name':'some name'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data['message'],'You are not authorized to perform this action')

        # Test customer can get their own user details
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('userdetail',args=(3,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'],'Successfully fetched user')

        # Test customer can edit their own name and email and not any other fields
        response =self.client.patch(reverse('userdetail',args=(3,)),data={'first_name':'some name'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'],'User details successfully updated!')
        response =self.client.patch(reverse('userdetail',args=(2,)),data={'role':'Admin'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_LoanListView(self):
        """Test fetching Loan list and creating loans by Agent """
        # Setup the token
        response,response_data=self.token_setup('agent@test.com','agent')
        token = response_data['access']

        # Test agent can create or edit loan
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data={'customerId':3,'loan_amount':100000 ,'tenure':12,'interest':8.5,'asset_value':1000000}
        response =self.client.post(reverse('loanlist'),data=data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        # Test customer get list of their own loans
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loanlist'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('loan' in response_data)
        

    
        """Test fetching Loan List by customers """
        # Setup the token
        response,response_data=self.token_setup('cust@test.com','cust')
        token = response_data['access']

        # Test customer get list of their own loans
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loanlist'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('loan' in response_data)
        # Test customer canot create loan
        response =self.client.post(reverse('loanlist'),data={'agent_name':'some name'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        """Test fetching Loan List by admins """
        # Setup the token
        response,response_data=self.token_setup('admin@test.com','admin')
        token = response_data['access']

        # Test admin get list of loans
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loanlist'))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('loan' in response_data)
        # Test admin canot create loan
        response =self.client.post(reverse('loanlist'),data={'agent_name':'some name'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_LoanDetailView(self):
        """Test fetching Loan detail and editing loans by Agent """
        # Setup the token
        response,response_data=self.token_setup('agent@test.com','agent')
        token = response_data['access']

        # Test agent can edit loan
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data={'loan_amount':10000}
        response =self.client.patch(reverse('loandetail',args=(1,)),data=data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
        # Test agent cannot edit approved loan
        response =self.client.patch(reverse('loandetail',args=(2,)),data=data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
        # Test agent get loan details 
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loandetail',args=(2,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('loan' in response_data)

        """Test fetching Loan detail and editing only state of loans by Admin """
        # Setup the token
        response,response_data=self.token_setup('admin@test.com','admin')
        token = response_data['access']

        # Test admin get loan details 
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loandetail',args=(2,)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('loan' in response_data)

        # Test admin can edit state of loan
        data={'state':'Approved'}
        response =self.client.put(reverse('loandetail',args=(2,)),data=data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
        self.assertEqual(response_data['loan']['state'],'Approved' )

    def test_LoanFilterView(self):
        """ Test fetching loans by filter for ADMIN"""
        # Setup the token 
        response,response_data=self.token_setup('admin@test.com','admin')
        token = response_data['access']

        # Test admin can view all loans by selected filters 
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loanfilter',args=('state','Approved')))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response =self.client.get(reverse('loanfilter',args=('created_date',str(date.today()))))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['loan']),Loan.objects.filter(created_date=date.today()).count())

        response =self.client.get(reverse('loanfilter',args=('modified_date',str(date.today()))))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['loan']),Loan.objects.filter(modified_date=date.today()).count())
        
        """ Test fetching loans by filter for AGENT """
        # Setup the token
        response,response_data=self.token_setup('agent@test.com','agent')
        token = response_data['access']

        # Test agent can view any loan by selected filter
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loanfilter',args=('created_date',str(date.today()))))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['loan']),Loan.objects.filter(modified_date=date.today()).count())
        
        response =self.client.get(reverse('loanfilter',args=('modified_date',str(date.today()))))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['loan']),Loan.objects.filter(modified_date=date.today()).count())

        response =self.client.get(reverse('loanfilter',args=('state','Approved')))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

        """ Test fetching and editing only their own loans by selected flters for CUSTOMERS """
        # Setup the token
        response,response_data=self.token_setup('cust@test.com','cust')
        token = response_data['access']

        # Test customer get only their own loans
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.get(reverse('loanfilter',args=('state','New',)))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response =self.client.get(reverse('loanfilter',args=('created_date',str(date.today()))))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['loan']),Loan.objects.filter(customerId=self.customer.id,created_date=date.today()).count())
        #chek response does not contain any other customers loan details
        values=[i['customerId'] for i in response_data['loan'] ]
        self.assertTrue(self.customer.id in values)
        self.assertFalse(self.customer2.id in values)


        response =self.client.get(reverse('loanfilter',args=('modified_date',str(date.today()))))
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['loan']),Loan.objects.filter(customerId=self.customer.id,modified_date=date.today()).count())
        values=[i['customerId'] for i in response_data['loan'] ]
        self.assertTrue(self.customer.id in values)
        self.assertFalse(self.customer2.id in values)

    def test_logout(self):
        """Test user can logout of all sessions """
        response,response_data=self.token_setup('cust@test.com','cust')
        token = response_data['access']
        
        # Test customer can logout safely from alll sessions
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response =self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response,response_data=self.token_setup('cust@test.com','cust')
        token2 = response_data['access']
        self.assertNotEqual(token,token2)
        #test previous token before logout is not valid even though it did not expire
        self.assertFalse(self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token))