import random
from django.core.cache import cache
import json

OTP_TIMEOUT = 300
ATTEMPTS_TIMEOUT = 300
MAX_ATTEMPTS = 3

class OTPService:

    @staticmethod
    def get_otp_key(phone_number: str) -> str:
        return f"otp:{phone_number.strip()}"

    @staticmethod
    def get_attempts_key(phone_number: str) -> str:
        return f"attempts:{phone_number.strip()}"

    @staticmethod
    def generate_otp_code(length : int = 6) -> str:
        start_range = 10 ** (length-1)
        end_range = (10 ** length) - 1

        otp = str(random.randint(start_range, end_range))
        return otp


    @staticmethod
    def save_otp_data_to_cache(phone_number: str) -> str:
        otp_code = OTPService.generate_otp_code()
        data = {
            "code": otp_code
        }

        key = OTPService.get_otp_key(phone_number)
        value = json.dumps(data)
        cache.set(key, value, OTP_TIMEOUT)

        return otp_code

    @staticmethod
    def get_otp_data(phone_number: str):
        key = OTPService.get_otp_key(phone_number)
        data = cache.get(key)
        if data:
            return json.loads(data)
        return None

    @staticmethod
    def delete_otp_data(phone_number: str) -> None:
        cache.delete(OTPService.get_otp_key(phone_number))
        cache.delete(OTPService.get_attempts_key(phone_number))

    @staticmethod
    def check_max_attempts(phone_number: str) -> bool:
        attempts = cache.get(OTPService.get_attempts_key(phone_number))
        print(attempts)
        return attempts is not None and attempts >= MAX_ATTEMPTS

    @staticmethod
    def increment_attempts(phone_number: str) -> None:
        attempts_key = OTPService.get_attempts_key(phone_number)
        try:
            current_attempts = cache.incr(attempts_key)
        except ValueError:
            cache.set(attempts_key, 1, ATTEMPTS_TIMEOUT)
            current_attempts = 1

        if current_attempts >= MAX_ATTEMPTS:
            OTPService.delete_otp_data(phone_number)





