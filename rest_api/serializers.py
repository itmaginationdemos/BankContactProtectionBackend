from rest_framework import serializers

from core.models import CustomUser
from verification.models import VerificationRequest


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'is_active', 'is_staff', 'phone_number', ]


class VerificationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = ['id', 'valid', 'requester', 'given', 'time', 'timeout', 'requester_verification_code',
                  'given_verification_code', 'status']


class RequestVerificationSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        # Nothing to do.
        pass

    def create(self, validated_data):
        # Nothing to do.
        pass

    phone_number = serializers.CharField(allow_null=False, allow_blank=False)
