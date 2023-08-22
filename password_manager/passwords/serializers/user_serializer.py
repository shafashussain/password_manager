from rest_framework import serializers
from ..models.user_model import UserModel, UserLoginModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLoginModel
        fields = "__all__"
