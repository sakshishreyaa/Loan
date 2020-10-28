import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager
import datetime
import numpy_financial as npf

# User model
class User(AbstractBaseUser, PermissionsMixin):

    # These fields tie users to the roles!
    ADMIN = 1
    AGENT = 2
    CUSTOMER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (AGENT, 'Agent'),
        (CUSTOMER, 'Customer')
    )
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # Roles created here
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    password=models.CharField(max_length=100)
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def jwt_get_secret_key(self):
        return self.jwt_secret


class Loan(models.Model):
    STATES=[
        ('New', 'New'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),

    ]

    customerId=models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer')
    agentId=models.ForeignKey(User,on_delete=models.CASCADE,related_name='agent')
    state=models.CharField(max_length=10,choices=STATES,default='New')
    # customer specific details
    loan_amount = models.IntegerField()
    tenure=models.IntegerField()
    interest=models.FloatField()
    created_date=models.DateField(auto_now_add=True)
    modified_date=models.DateField(auto_now=True)
    asset_value = models.FloatField()    #asset for which loan is needed

    def __str__(self):
        return self.customerId

    
    def LTV_ratio(self):
        ltv=str((self.loan_amount / self.asset_value) * 100 ) +"%"
        return ltv

    def EMI(self):
        if self.state=="Approved":
            interest=self.interest/(100*12)
            emi=npf.pmt(interest,self.tenure,self.loan_amount)
            return -1*round(emi,0)
        return None