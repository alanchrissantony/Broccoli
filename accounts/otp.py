from django_otp.oath import TOTP
from django_otp.util import random_hex
import time

class TOTPVerification:

    def __init__(self, key=None, number_of_digits=6, token_validity_period=60):  # 1 minute in seconds
        self.key = key or random_hex(20).encode('utf-8')
        self.number_of_digits = number_of_digits
        self.token_validity_period = token_validity_period
        self.last_verified_counter = -1
        self.verified = False

    def totp_obj(self):
        totp = TOTP(key=self.key,
                    step=self.token_validity_period,
                    digits=self.number_of_digits)
        totp.time = time.time()
        return totp

    def generate_token(self):
        totp = self.totp_obj()
        otp = str(totp.token()).zfill(self.number_of_digits)
        return otp

    def verify_token(self, token, tolerance=0):
        try:
            token = int(token)
        except ValueError:
            return False

        totp = self.totp_obj()
        current_counter = totp.t()
        if current_counter > self.last_verified_counter and totp.verify(token, tolerance=tolerance):
            self.last_verified_counter = current_counter
            self.verified = True
            return True
        else:
            self.verified = False
            return False