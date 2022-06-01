import datetime
import random

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from django.db.models import Q
from django.db import transaction
from phone_field.phone_number import PhoneNumber
from django.shortcuts import get_object_or_404
from django.conf import settings

from core.models import CustomUser
from verification.models import VerificationRequest
from .serializers import CustomUserSerializer, VerificationRequestSerializer, RequestVerificationSerializer


class ActiveUserViewSet(viewsets.ReadOnlyModelViewSet):
    model = CustomUser
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class VerificationRequestsViewSet(viewsets.ReadOnlyModelViewSet):
    model = VerificationRequest
    serializer_class = VerificationRequestSerializer

    def get_queryset(self):
        return VerificationRequest.objects.filter(
            (Q(requester=self.request.user) | Q(given=self.request.user)) & Q(valid=True)
            & Q(timeout__gte=datetime.datetime.now())
        )

    @action(detail=False, methods=['post'])
    def request_verification(self, request):
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Not allowed to perform this action.")

        serializer = RequestVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = PhoneNumber(serializer.validated_data.get('phone_number'))
            phone_number.parse()
            if user.phone_number == phone_number:
                raise PermissionDenied("Not allowed to request verification for own number.")
            given = get_object_or_404(CustomUser, phone_number=phone_number)

            # Timeouts
            time = datetime.datetime.now()
            timeout_delta = datetime.timedelta(minutes=settings.VERIFICATION_TIMEOUT_MINUTES)
            timeout = time + timeout_delta

            # Verification codes
            requester_verification_code = random.randint(
                settings.VERIFICATION_CODE_MIN_VALUE,
                settings.VERIFICATION_CODE_MAX_VALUE
            )
            given_verification_code = random.randint(
                settings.VERIFICATION_CODE_MIN_VALUE,
                settings.VERIFICATION_CODE_MAX_VALUE
            )

            new_verification_request = VerificationRequest(
                requester=user,
                given=given,
                time=time,
                timeout=timeout,
                requester_verification_code=requester_verification_code,
                given_verification_code=given_verification_code
            )

            # Invalidate previous Verifications for these users
            with transaction.atomic():
                VerificationRequest.objects.filter(valid=True, requester=user, given=given).update(valid=False)
                new_verification_request.save()

            response_serializer = VerificationRequestSerializer(new_verification_request)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_verified_by_requester(self, request, pk=None):
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Not allowed to perform this action.")

        verification_request = self.get_object()
        if verification_request.requester == user:
            verification_request.status = VerificationRequest.VerificationStatus.VERIFIED_BY_REQUESTER
            verification_request.save()
            return Response({'status': 'status set'})
        else:
            raise PermissionDenied("Not allowed to perform this action.")

    @action(detail=True, methods=['post'])
    def set_verified_by_given(self, request, pk=None):
        user = self.request.user
        verification_request = self.get_object()

        if verification_request.given == user:
            verification_request.status = VerificationRequest.VerificationStatus.VERIFIED_BY_GIVEN
            verification_request.save()
            return Response({'status': 'status set'})
        else:
            raise PermissionDenied("Not allowed to perform this action.")