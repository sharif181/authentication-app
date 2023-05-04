import os

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics
from rest_framework import permissions, status
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_email, account_activation_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Create your views here.
from .models import User
from .serializers import (
    UserSerializer,
    # LoginSerializer,
    # LogoutSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer
)


class UserListView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serialize = UserSerializer(users, many=True)
        return Response(serialize.data)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data

        # create, validate, save
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():  # invoke validate()
            serializer.save()

            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            current_site = get_current_site(request).domain
            send_email(current_site, user, user.email)
            # # token = RefreshToken.for_user(user).access_token
            # relative_link = reverse('user:email_verify')
            # absolute_url = f'http://{current_site}{relative_link}' \
            #                f'?token={str(token)}'
            # email_body = f'Hi, {user.username}! Use link below to verify email' \
            #              f'your email:\n{absolute_url}'
            # data = {
            #     'email_body': email_body,
            #     'email_subject': 'Verify your Cluvii e-mail',
            #     'to_email': user.email,
            # }

            # Util.send_email(data)

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#
#     # renderer_classes = (UserRenderer,)
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)  # User data
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class LogoutView(generics.GenericAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     # renderer_classes = (UserRenderer,)
#     serializer_class = LogoutSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)

@api_view()
def activateView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return Response('Thank you for your email confirmation. Now you can login your account.',
                        status=status.HTTP_200_OK)
    else:
        return Response('Activation link is invalid!', status=status.HTTP_400_BAD_REQUEST)


class TokenObtainPairViewOverwrite(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        if request.data.get('email') == '' or request.data.get('password') == '':
            return Response("Email and Password field can not be empty", status=status.HTTP_200_OK)
        user = User.objects.filter(email=request.data.get('email')).first()
        if user is None:
            return Response("User doesn't exist", status=status.HTTP_204_NO_CONTENT)
        if user.is_verified:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response("Invalid user name and password", status=status.HTTP_400_BAD_REQUEST)
        return Response("Your account is not verified yet", status=status.HTTP_400_BAD_REQUEST)
