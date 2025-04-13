from rest_framework import serializers
from .models import User, EmailOTP


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'number', 'password', 'password2', 'otp']
        extra_kwargs = {'password': {'write_only': True}}

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
