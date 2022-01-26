from django.contrib import auth
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import User
from .serializers import RegistrationSerializer, LoginSerializer

from drf_spectacular.utils import extend_schema


# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [OrderingFilter]
    ordering_fields = ['first_name', 'last_name', 'birth_date', 'email']
    ordering = "last_name"  # Default ordering


@extend_schema(
    request=RegistrationSerializer,
    description="Date formats: DD-MM-YYYY, DD.MM.YYYY, YYYY-MM-DD, YYYY.MM.DD",
)
class Registration(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"message": "You already have an account"})
        try:
            serializer = RegistrationSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                account.save()
                token = Token.objects.get_or_create(user=account)[0].key
                data['message'] = "Successfully registered a new user."
                data['email'] = account.email
                data["token"] = token
            else:
                data = serializer.errors
        except KeyError as e:
            raise ValidationError({'message': 'All fields are required'})
        return Response(data)


@extend_schema(
    request=LoginSerializer,
)
class Login_user(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"message": "You are already logged in."})
        data = {}
        body = request.data
        try:
            email = body['email']
            password = body['password']
            user = User.objects.get(email=email)
            token = Token.objects.get_or_create(user=user)[0].key
        except BaseException as e:
            raise ValidationError({'message': f'Bad request - Invalid data: {str(e)}'})

        if not user.check_password(password):
            raise ValidationError(
                {'message': "Incorrect login information. Please check your credentials and try again."})
        if user:
            if user.is_active:
                auth.login(request, user)
                data['message'] = "User logged in."
                data['email'] = user.email
                data['token'] = token

                return Response(data, status=status.HTTP_200_OK)
            else:
                raise ValidationError({'message': f'Account not active'})
        else:
            raise ValidationError({'message': f'User does not exist'})


class LogoutUser(APIView):
    serializer_class = None
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        try:
            request.user.auth_token.delete()
            auth.logout(request)
            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except AttributeError as e:
            return Response({"message": "You must be logged in first."})
