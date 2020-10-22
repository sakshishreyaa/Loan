from .models import User,Loan
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from django.contrib.auth.models import update_last_login

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
        fields = (
            'email',
            'role','first_name','last_name'
        )

        # def update(self, instance, validated_data):
        #     """ 
        #     Update and return an existing user instance, given the validated data.
        #     """
        #     instance.email = validated_data.get('email', instance.email)
        #     instance.role = validated_data.get('role', instance.role)
        #     instance.first_name = validated_data.get('first_name', instance.first_name)
        #     instance.last_name = validated_data.get('last_name', instance.last_name)
        #     instance.save()
        #     return instance
class LoanAgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields="__all__"
        read_only_fields=['AgentId','state']



class LoanCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Loan
        fields=['customerId','agentId','amount_required','tenure','interest','state']
        #read_only_fields=['customerId','agentId','amount_required','tenure','interest','state']

class LoanAdminSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Loan
        fields='__all__'
        read_only_fields=['id','customerId','agentId','amount_required','tenure','interest']
        