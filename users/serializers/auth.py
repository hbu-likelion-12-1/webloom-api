from rest_framework import serializers
from users.models import User


class AuthSerializer:
    class Signup(serializers.Serializer):
        username = serializers.CharField(required=True)
        sex = serializers.CharField(required=True)
        birthday = serializers.DateField(required=True)
        region = serializers.CharField(max_length=20)
        city = serializers.CharField(max_length=20)
        town = serializers.CharField(max_length=20)
        period = serializers.CharField(max_length=30)
        care_status = serializers.CharField(max_length=30)
        cause = serializers.CharField(max_length=30)
        cost = serializers.CharField(max_length=30)
        workplace_comprehension = serializers.CharField(max_length=30)
        communication = serializers.CharField(max_length=30)
        depression_test = serializers.JSONField()
        kakao_id = serializers.CharField()

        def signup(self, validated_data):
            return User.create(validated_data)

    class Login:
        pass
