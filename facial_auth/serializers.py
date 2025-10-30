from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, SecurityArea, AccessLog, VisitorLog, SystemSettings
from datetime import datetime, timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SecurityAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityArea
        fields = ['id', 'name', 'description', 'access_level']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    allowed_areas = SecurityAreaSerializer(many=True, read_only=True)
    pass_status = serializers.SerializerMethodField()
    days_until_expiry = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'security_number', 'user_type', 'access_level',
            'pass_issued', 'pass_expires', 'is_active', 'pass_status',
            'days_until_expiry', 'department', 'position', 'allowed_areas'
        ]

    def get_pass_status(self, obj):
        return obj.is_pass_valid()

    def get_days_until_expiry(self, obj):
        return obj.days_until_expiry()


class AccessLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    security_area = SecurityAreaSerializer(read_only=True)

    class Meta:
        model = AccessLog
        fields = [
            'id', 'user', 'security_area', 'access_granted',
            'access_time', 'access_point', 'reason_denied', 'authentication_method'
        ]


class VisitorLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    areas_visited = SecurityAreaSerializer(many=True, read_only=True)

    class Meta:
        model = VisitorLog
        fields = [
            'id', 'user', 'visit_date', 'entry_time', 'exit_time',
            'purpose', 'hosting_staff', 'areas_visited'
        ]


class FaceRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    security_number = serializers.CharField()
    face_data = serializers.ListField(child=serializers.FloatField())
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPES)
    access_level = serializers.IntegerField(
        min_value=1, max_value=5, default=1)
    pass_duration_days = serializers.IntegerField(
        min_value=1, max_value=365, default=30)


class AuthenticationSerializer(serializers.Serializer):
    security_number = serializers.CharField()
    face_data = serializers.ListField(child=serializers.FloatField())
    security_area_id = serializers.IntegerField(required=False)


class AdminUserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPES)
