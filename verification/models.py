from django.db import models
from core.models import CustomUser
from django.utils.translation import gettext_lazy as _


class VerificationRequest(models.Model):
    class VerificationStatus(models.TextChoices):
        REQUESTED = 'RQ', _('Requested')
        VERIFIED_BY_REQUESTER = 'VR', _('Verified by requester')
        VERIFIED_BY_GIVEN = 'VG', _('Verified by given')

    valid = models.BooleanField(null=False, default=True)
    requester = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE,
                                  related_name='verificationRequests')
    given = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE,
                              related_name='verificationGivens')
    time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    timeout = models.DateTimeField(null=False, blank=False)
    requester_verification_code = models.CharField(max_length=255, null=False, blank=False)
    given_verification_code = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(
        max_length=2,
        choices=VerificationStatus.choices,
        default=VerificationStatus.REQUESTED
    )
