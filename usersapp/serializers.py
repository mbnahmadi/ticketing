from rest_framework import serializers
from .models import UserModel
from django.core.exceptions import ValidationError

class SignUpserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "username", "password", "phone_number", "gender"] 

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("the password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        return UserModel.objects.create_user(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            username = validated_data["username"],
            password = validated_data["password"],
            phone_number = validated_data["phone_number"],
            gender = validated_data["gender"],
        )

