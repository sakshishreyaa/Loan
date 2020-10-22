import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager

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
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Loan(models.Model):
    STATES=[
        ('New', 'New'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),

    ]
    customerId=models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer')
    agentId=models.ForeignKey(User,on_delete=models.CASCADE,related_name='agent')
    state=models.CharField(max_length=10,choices=STATES,default='New')
    amount_required = models.IntegerField()
    tenure=models.IntegerField()
    interest=models.FloatField()

    def __str__(self):
        return self.customerId


