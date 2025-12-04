from django.utils import timezone

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.service import OTPService
from .models import uzb_phone_validator
from django.contrib.auth import get_user_model

User = get_user_model()


class StartRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=13,
        validators=[uzb_phone_validator],
        write_only=True,
        label="Telefon raqami"
    )


    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        otp_code = OTPService.save_otp_data_to_cache(phone_number)
        validated_data['otp_code'] = otp_code

        return validated_data


class VerifyRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=13,
        validators=[uzb_phone_validator],
        write_only=True,
        label="Telefon raqami"
    )

    otp_code = serializers.CharField(
        min_length=6,
        max_length=6,
        write_only=True,
        label="otp kodi"
    )

    user_id = serializers.IntegerField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        otp_code = attrs.get('otp_code')

        if OTPService.check_max_attempts(phone_number):
            raise ValidationError("Maksimal urinishlar soni tugadi, Iltimos qayta kod so'rang.")

        otp_data = OTPService.get_otp_data(phone_number)

        if otp_data is None:
            raise ValidationError("Bu raqam bilan user malumot yo'q yoki otp muddati tugagan.")

        if otp_code != otp_data.get('code'):
            OTPService.increment_attempts(phone_number)
            if OTPService.check_max_attempts(phone_number):
                raise ValidationError("Noto'g'ri kod. Maksimal urinish soni tugadi. Yangi kod so'rang.")

            raise ValidationError("Noto'g'ri OTP kodi.")

        OTPService.delete_otp_data(phone_number)

        try:
            user, created = User.objects.get_or_create(phone_number=phone_number, defaults={
                'date_joined': timezone.now()
            })
        except IntegrityError:
            raise ValidationError("User yaratishda xato ro/'y berdi")

        refresh = get_token_for_user(user)

        attrs['user'] = user
        attrs['refresh'] = refresh['refresh']
        attrs['access'] = refresh['access']

        return attrs


def get_token_for_user(user):
    tokens = RefreshToken.for_user(user)
    access = tokens.access_token

    access['role'] = user.role

    return {
        'access': str(access),
        'refresh': str(tokens)
    }



