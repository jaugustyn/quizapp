from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError
from .models import User
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'password']

        extra_fields = {'password': {"write_only": True}}

    def save(self, **kwargs):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        # try:
        #     password_validation.validate_password(password=password, user=user)
        # except ValidationError:
        #     raise ValidationError({'message': "Password requires sth"})

        user.set_password(password)
        user.save()
        return user
