from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework import exceptions

from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    # def create(self, validated_data):
    #     try:
    #         validate_password(validated_data["password"])
    #         user = User(
    #             email=validated_data["email"],
    #             name=validated_data["name"],
    #             phone_number=validated_data["phone_number"],
    #         )
    #     except Exception as e:
    #         raise exceptions.ParseError(e)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def create(self, validated_data):
        try:
            validate_password(validated_data["password"])
        except Exception as error:
            raise exceptions.ParseError(error)

        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
