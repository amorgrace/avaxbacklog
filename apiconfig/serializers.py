from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *



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
            password=validated_data['password'],  
            fullname=validated_data['fullname']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'fullname', 'email', 'main', 'profit', 'total')
        extra_kwargs = {
            'id': {'read_only': True},
            'main': {'read_only': True},
            'profit': {'read_only': True},
            'fullname': {'read_only': True},
            'email': {'read_only': True},
            
        }

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = ('key', 'user')
        extra_kwargs = {'key': {'read_only': True}}


class RecentTransactionSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField

    class Meta:
        model = RecentTransaction
        fields = '__all__'

    def get_time_since_created(self, obj):
        return obj.time_since_created()
    

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class WithdrawalSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    crypto_type = serializers.ChoiceField(choices=RecentTransaction.CRYPTO_CHOICES, required=True)
    withdrawal_address = serializers.CharField(required=True)

    class Meta:
        model = RecentTransaction
        fields = ["amount", "crypto_type", "withdrawal_address"]

    def validate(self, data):
        user = self.context["request"].user
        amount = data["amount"]

        if user.total < amount:
            raise serializers.ValidationError({
                "error": "Insufficient balance for this withdrawal."
            })

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        amount = validated_data["amount"]

        if user.main >= amount:
            user.main -= amount
        else:
            diff = amount - user.main
            user.main = 0
            user.profit -= diff

        user.save()

        return RecentTransaction.objects.create(
            user=user,
            crypto_type=validated_data["crypto_type"],
            withdrawal_address=validated_data["withdrawal_address"],
            amount=validated_data["amount"],
            transaction_type="withdrawal",
            transaction_status="pending",
        )


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['user', 'kyc_status', 'image_url', 'created_at']
        read_only_fields = ['kyc_status']
