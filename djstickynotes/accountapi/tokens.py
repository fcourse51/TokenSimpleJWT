from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta


def create_jwt_pair_for_user(user):
    refresh = RefreshToken.for_user(user)
    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
    return tokens


def expire_tokens(user):
    try:
        refresh_token = RefreshToken.for_user(user)

        now = timedelta(seconds=120)
        # now = datetime.now()
        # future = timedelta(seconds=5)+datetime.now()
        # expiry =  future - current
        # now = expiry

        # Expire refresh token
        refresh_token.set_exp(lifetime=now)

        # Expire access token
        access_token = refresh_token.access_token
        access_token.set_exp(lifetime=now)

        print("Token Expired !!", {
        "access_token": str(access_token),
        "access_exp": access_token.payload.get("exp"),
        "refresh_token": str(refresh_token),
        "payload": access_token})

    except Exception as e:
        import sys, os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, str(e))




    