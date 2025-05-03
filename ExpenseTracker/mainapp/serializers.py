from rest_framework import serializers
from .models import User, EmailOTP
from .models import Donation
from .models import Transactions, Bill, RecurringExpense, Budget


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'number', 'password', 'password2', 'otp']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered. Please log in or use another.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")

        try:
            otp_record = EmailOTP.objects.get(email=attrs['email'], otp=attrs['otp'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('otp')
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'number', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs


class EmailOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOTP
        fields = ['email', 'otp']
        

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'name', 'email', 'amount', 'transaction_id']        
        

#Anamika
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['user', 'type', 'subtype', 'amount', 'description', 'timestamp']

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'        