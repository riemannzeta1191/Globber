from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import GlobberUser
# Create your views here.


class SignUp(APIView):
    permission_classes = (AllowAny,)
    """
    Creates an User
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                result = serializer.data
                result['token'] = token.key
                return Response(result, status=status.HTTP_201_CREATED)


class SignIn(APIView):
    """
    Logs in an user
    """
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        if username and password:
            try:
                queryset = GlobberUser.objects.get(username=username)
                id = queryset.id
                if request.user.id == id:
                    user = authenticate(username=username,password=password)
                    try:
                        if user.is_active:
                            login(request,user)
                            return Response(status=status.HTTP_200_OK)
                    except AttributeError:
                        return Response(status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self,request):
        username = request.data["username"]
        password = request.data["password"]
        logout(request)
        return Response(status=status.HTTP_200_OK)
