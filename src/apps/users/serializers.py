from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True  # password is hidden on response
    )
    confirm_password = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True  # password is hidden on response
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password',)

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'Username can only contain alphanumeric characters. '
            )

        return attrs

    # create a new user
    def create(self, validated_data):
        if validated_data.get('confirm_password') != validated_data.get('password'):
            raise serializers.ValidationError('Password not matched')
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


# class LoginSerializer(serializers.ModelSerializer):
# 	email = serializers.EmailField(max_length=255, min_length=3)
# 	password = serializers.CharField(
# 		max_length=68,
# 		min_length=8,
# 		write_only=True
# 	)
# 	username = serializers.CharField(
# 		max_length=255,
# 		min_length=3,
# 		read_only=True
# 	)
# 	tokens = serializers.SerializerMethodField()
#
# 	class Meta:
# 		model = User
# 		fields = ('email', 'password', 'username', 'tokens')
#
# 	def get_tokens(self, obj):
# 		user = User.objects.get(email=obj['email'])
#
# 		return {
# 			'access': user.tokens()['access'],
# 			'refresh': user.tokens()['refresh']
# 		}
#
# 	def validate(self, attrs):
# 		email = attrs.get('email', '')
# 		password = attrs.get('password', '')
#
# 		user = auth.authenticate(email=email, password=password)
#
# 		if not user:
# 			raise AuthenticationFailed(
# 				'Invalid credentials. Please try again.'
# 			)
# 		if not user.is_active:
# 			raise AuthenticationFailed(
# 				'Account disabled.'
# 			)
# 		if not user.is_verified:
# 			raise AuthenticationFailed('Email is not verified.')
#
# 		return {
# 			'email': user.email,
# 			'username': user.username,
# 			'tokens': user.token()
# 		}

# class LogoutSerializer(serializers.Serializer):
# 	refresh = serializers.CharField()
#
# 	default_error_messages = {
# 		'bad_token': 'Token is expired or invalid'
# 	}
#
# 	def validate(self, attrs):
# 		self.token = attrs['refresh']
# 		return attrs
#
# 	def save(self, **kwargs):
# 		try:
# 			RefreshToken(self.token).blacklist()
# 		except TokenError:
# 			self.fail('Bad Token')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'is_verified')
        # read_only_fields = ['tokens']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
