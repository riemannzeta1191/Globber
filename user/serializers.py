from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator,ValidationError
from .models import GlobberUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobberUser
        fields = ('id', 'name','username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    name = serializers.CharField(

    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=GlobberUser.objects.all())],
        required=True
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = GlobberUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



