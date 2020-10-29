from .models import User,Loan
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from django.contrib.auth.models import update_last_login
from rest_framework.fields import CurrentUserDefault


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class LoanAgentSerializer(serializers.ModelSerializer):
    agent_name=serializers.SerializerMethodField('get_agent_name')
    customer_name=serializers.SerializerMethodField('get_customer_name')
    
    class Meta:
        model = Loan
        fields='__all__'
        read_only_fields=['agentId','state'] 

    def get_agent_name(self,obj):
        pk=obj.agentId_id
        data=User.objects.get(pk=pk)
        name=data.first_name+data.last_name
        return name   
    def get_customer_name(self,obj):
        pk=obj.customerId_id
        data=User.objects.get(pk=pk)
        name=data.first_name+data.last_name
        return name
    
    




class LoanCustomerSerializer(serializers.ModelSerializer):
    agent_name=serializers.SerializerMethodField('get_agent_name')
    customer_name=serializers.SerializerMethodField('get_customer_name')
    EMI=serializers.SerializerMethodField()


    class Meta:
        model = Loan
        fields=['customer_name','agent_name','loan_amount','tenure','interest','state','EMI']
        #read_only_fields=['customerId','agentId','amount_required','tenure','interest','state']
    
    def get_agent_name(self,obj):
        pk=obj.agentId_id
        data=User.objects.get(pk=pk)
        name=data.first_name+data.last_name
        return name   
    def get_customer_name(self,obj):
        pk=obj.customerId_id
        data=User.objects.get(pk=pk)
        name=data.first_name+data.last_name
        return name
    def get_EMI(self,obj):
        if obj.state=="Approved":
            return obj.EMI()
        return "Not Applicable"

class LoanAdminSerializer(serializers.ModelSerializer):
    LTV_ratio=serializers.SerializerMethodField()
    agent_name=serializers.SerializerMethodField('get_agent_name')
    customer_name=serializers.SerializerMethodField('get_customer_name')
    
    class Meta:
        model = Loan
        fields='__all__'
        read_only_fields=['customer_name','agent_name','loan_amount','tenure','interest','EMI']

    def get_LTV_ratio(self,obj):
        return obj.LTV_ratio()
    def get_agent_name(self,obj):
        pk=obj.agentId_id
        data=User.objects.get(pk=pk)
        name=data.first_name+data.last_name
        return name   
    def get_customer_name(self,obj):
        pk=obj.customerId_id
        data=User.objects.get(pk=pk)
        name=data.first_name+data.last_name
        return name
        