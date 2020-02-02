from rest_framework import serializers
from apps.user_registration.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user', 'email', 'first_name', 'last_name',)
