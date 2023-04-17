from rest_framework import serializers
from api.models import Tasks
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    created_date=serializers.DateTimeField(read_only=True)
    status=serializers.BooleanField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Tasks
        fields="__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","first_name","last_name","email"]