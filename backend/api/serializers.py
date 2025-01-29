from rest_framework import serializers
from .models import User, Activity, UserEntry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'created_at']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'category', 'co2_per_unit']

class UserEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # optional: show user details in response
    activity = ActivitySerializer(read_only=True)

    class Meta:
        model = UserEntry
        fields = ['id', 'user', 'activity', 'quantity', 'date', 'total_co2']
