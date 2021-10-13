from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, generics, status
from .models import User
from .serializers import RegistrationSerializer
from .forms import RegistrationForm


# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


@api_view(['POST'])
def registration_view(request):
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


# {
# "first_name": "test1",
# "last_name": "test214",
# "email":"test1@gmail.com",
# "password":"1234",
# "birth_date":"2010-10-20"
# }