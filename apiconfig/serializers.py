from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



CustomUser = get_user_model()  # Call the function to get the model

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'fullname', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],  # Fix typo
            fullname=validated_data['fullname']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'fullname', 'email', 'main', 'profit', 'total', 'kyc_status',)
        extra_kwargs = {
            'id': {'read_only': True},
            'main': {'read_only': True},
            'profit': {'read_only': True},
            'kyc_status': {'read_only': True},
            'fullname': {'read_only': True},
            'email': {'read_only': True},
            
        }

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = ('key', 'user')
        extra_kwargs = {'key': {'read_only': True}}