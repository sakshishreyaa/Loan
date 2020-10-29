import uuid
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import Http404
from rest_framework.decorators import api_view
import datetime
from django.utils import timezone


from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    LoanAdminSerializer,
    LoanAgentSerializer,
    LoanCustomerSerializer
)

from .models import User,Loan


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

class UserListView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
    
class UserDetailView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request,pk):
        user = request.user
        if user.role == 3:
            if user.id == pk:
                response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched user',
                'user': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'You are not authorized to perform this action'
                }
                return Response(response, status.HTTP_401_UNAUTHORIZED)
        else:

            data = self.get_object(pk)
            serializer = self.serializer_class(data)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched user',
                'user': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        data = self.get_object(pk)
        serializer = self.serializer_class(data,data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:

            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User details successfully updated!',
                'user': serializer.data
            }
            return Response(response, status=status_code)
        
        
class CustomerLoanView(APIView):
    #serializer_class=LoanSerializer
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanCustomerSerializer
    

    def get(self,request):
        user=request.user
        if user.role==3:
    
            #cust_id=User.objects.get(user.id)
            loans=Loan.objects.filter(customerId=user.id)
            serializer = self.serializer_class(loans, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched loans',
                'loans': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class AgentLoanView(APIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanAgentSerializer

    def get(self,request):
        user=request.user
        if user.role==2:
            loans = Loan.objects.all()
            serializer = LoanAgentSerializer(loans, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched loans',
                'loans': serializer.data,

            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self,request):
        user=request.user
        if user.role==2:
            serializer=self.serializer_class(data=request.data,context={'request':request})
            valid=serializer.is_valid(raise_exception=True)

            if valid:
                serializer.save(agentId=request.user)
                status_code=status.HTTP_200_OK
                response = {
                'success': True,
                'status_code': status_code,
                'message': 'Successfully created loan request',
                'loan': serializer.data,
                
                

            }
                return Response(response,status=status_code)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"message":"You ar not authorized to perform this action"},status=status.HTTP_401_UNAUTHORIZED)
            
        

class AgentLoanDetailView(APIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanAgentSerializer

    def get_object(self,pk):
        try:
            return Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        user=request.user
        if user.role==2:
            try:
                loans = Loan.objects.get(pk=pk)
                serializer = self.serializer_class(loans)
                response = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Successfully fetched loan',
                    'loans': serializer.data

                }
                return Response(response, status=status.HTTP_200_OK)
            except Loan.DoesNotExist:
                raise Http404
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk):
        user=request.user
        if user.role==2:
            loan = self.get_object(pk)
            if loan.state=="New":
                serializer = self.serializer_class(loan,data=request.data,partial=True)
                valid = serializer.is_valid(raise_exception=True)
                if valid:

                    serializer.save()
                    status_code = status.HTTP_202_ACCEPTED

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Loan details successfully updated!',
                        'user': serializer.data,
                        
                    }
                    return Response(response, status=status_code)
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({ 'message' : "Loan cannot be edited after being approved or rejected"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


            


class AdminLoanView(APIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanAdminSerializer

    def get(self,request):
        user=request.user
        if user.role==1:
    
            loans=Loan.objects.all()
            serializer=self.serializer_class(loans,many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched loan',
                'loans': serializer.data

            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class AdminLoanDetailView(APIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanAdminSerializer

    def get_object(self,pk):
        try:
            return Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        user=request.user
        if user.role==1:
            try:
                loans = Loan.objects.get(pk=pk)
                serializer = self.serializer_class(loans)
                response = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Successfully fetched loan',
                    'loans': serializer.data

                }
                return Response(response, status=status.HTTP_200_OK)
            except Loan.DoesNotExist:
                raise Http404
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        user=request.user
        if user.role==1:
            data = self.get_object(pk)
            serializer = self.serializer_class(data,data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:

                serializer.save()
                status_code = status.HTTP_202_ACCEPTED

                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Loan details successfully updated!',
                    'user': serializer.data
                }
                return Response(response, status=status_code)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AdminAgentFilterView(APIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanAgentSerializer

    def get(self,request,filtr,value):
        user=request.user
        if user.role!=3:
            
            if filtr == "state":
                loans = Loan.objects.filter(state=value)
            elif filtr == "created_date":
                loans=Loan.objects.filter(created_date=datetime.datetime.strptime(value, "%Y-%m-%d").date())
            elif filtr == "modified_date":
                loans=Loan.objects.filter(modified_date=datetime.datetime.strptime(value, "%Y-%m-%d").date())
            else :
                response={"message":"invalid filter",
                "valid filter strings": "state  , created_date , modified_date" }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
            if not loans.exists():
                return Response({"message":"No records corresponding to given filter value"},status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(loans, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched loans based on filter',
                'loans': serializer.data,

            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class CustomerFilterView(APIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=LoanCustomerSerializer
    

    def get(self,request,filtr,value):
        user=request.user
        if user.role==3:

            if filtr == "state":
                loans = Loan.objects.filter(customerId=user.id,state=value)
            elif filtr == "created_date":
                loans=Loan.objects.filter(customerId=user.id,created_date=datetime.datetime.strptime(value, "%Y-%m-%d").date())
            elif filtr == "modified_date":
                loans=Loan.objects.filter(customerId=user.id,modified_date=datetime.datetime.strptime(value, "%Y-%m-%d").date())
            else :
                response={"message":"invalid filter",
                "valid filter strings": "state  , created_date , modified_date" }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
            if not loans.exists():
                return Response({"message":"No records corresponding to given filter value for the current user"},status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(loans, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched loans based on filter',
                'loans': serializer.data,

            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    """
    Use this endpoint to log out all sessions for a given user.
    """
    # the secret key used for generating jwt tokens is changed evry time a user logout so the same token cannot
    # be used for authentication after logout 
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response({"message":"user successfully logged out"},status=status.HTTP_204_NO_CONTENT)       
    
                