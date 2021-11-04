from django.contrib import auth
from rest_framework import viewsets, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import RegistrationSerializer


# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['first_name', 'last_name', 'birth_date', 'email']
    ordering = "last_name"  # Default ordering


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['response'] = "Successfully registered a new user."
            data['email'] = account.email
            data["token"] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    body = request.data
    email = body['email']
    password = body['password']
    try:
        user = User.objects.get(email=email)
    except BaseException:
        raise ValidationError({'400': f'{str(BaseException)}'})
    token = Token.objects.get_or_create(user=user)[0].key

    if not user.check_password(password):
        raise ValidationError({'message': "Incorrect login information. Please check your crefentials and try again."})

    if user:
        if user.is_active:
            auth.login(request, user)
            data['message'] = "User logged in."
            data['email'] = user.email

            return Response({'data': data, 'token': token})
        else:
            raise ValidationError({'400': f'Account not active'})
    else:
        raise ValidationError({'400': f'User does not exist'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    auth.logout(request)
    return Response("User logged out successfully.")
