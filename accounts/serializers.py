from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid response',
            value={
                "message": "Successfully registered a new user.",
                "email": "user@example.com",
                "token": "9944b09199c62bcf9418ad846dd0e4bbdfxxxxx",
            },
            request_only=False,
            response_only=True
        ),
    ]
)
class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True, input_formats=settings.DATE_INPUT_FORMATS)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'password']
        extra_fields = {'password': {"write_only": True}}

    def create(self, validated_data):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            birth_date=self.validated_data['birth_date'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()

        return user


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid response',
            value={
                "message": "User logged in.",
                "email": "user@example.com",
                "token": "9944b09199c62bcf9418ad846dd0e4bbdfxxxxx",
            },
            request_only=False,
            response_only=True
        ),
    ]
)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        fields = ["email", "password"]
