import secrets
from datetime import timedelta
import requests
from django.utils import timezone
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .models import ManagerOTP

# Ghasedak Settings
GHASEDAK_API_KEY = "P/gEN/k+t6qVTLRd1Fzede42XCe+wJjYkGsLKx2ZaGM"
GHASEDAK_URL = "https://api.ghasedaksms.com/v2/send/verify"


def normalize_phone(phone):
    if not phone:
        return ""
    phone = "".join(filter(str.isdigit, phone))
    if len(phone) == 10 and phone.startswith("9"):
        phone = "0" + phone
    if len(phone) == 12 and phone.startswith("98"):
        phone = "0" + phone[2:]
    if not (len(phone) == 11 and phone.startswith("09")):
        return ""
    return phone


class ManagerLoginStartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
        if not phone:
            return Response({"error": "Phone required"}, status=400)

        user, _ = User.objects.get_or_create(phone=phone)
        otp_code = f"{secrets.randbelow(900000) + 100000}"

        otp_obj, _ = ManagerOTP.objects.get_or_create(phone=phone)
        otp_obj.touch_new_code(code=otp_code, ttl_seconds=300)

        print(f"\n========== OTP for {phone}: {otp_code} ==========\n")

        payload = {
            "receptor": phone,
            "type": 1,
            "template": "AuthCode",
            "param1": str(otp_code),
        }
        headers = {
            "apikey": GHASEDAK_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            resp = requests.post(GHASEDAK_URL, data=payload, headers=headers, timeout=5)
            if resp.status_code in (200, 201, 202):
                return Response({"message": "OTP sent"}, status=200)
        except Exception:
            pass

        return Response({"message": "OTP generated (check console)"}, status=200)


class ManagerVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
        code = request.data.get("code")

        if not phone or not code:
            return Response({"error": "Phone and code required"}, status=400)

        try:
            otp_obj = ManagerOTP.objects.get(phone=phone)
        except ManagerOTP.DoesNotExist:
            return Response({"error": "OTP not found"}, status=400)

        if otp_obj.is_expired():
            otp_obj.delete()
            return Response({"error": "OTP expired"}, status=400)

        if str(otp_obj.code) != str(code):
            otp_obj.increment_attempts()
            return Response({"error": "Invalid code"}, status=400)

        otp_obj.delete()
        user, created = User.objects.get_or_create(phone=phone)
        user.is_center_manager = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "success": True,
                "is_center_manager": True,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=200,
        )


class VisitorLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
        if not phone:
            return Response({"error": "Phone required"}, status=400)

        user, created = User.objects.get_or_create(
            phone=phone, defaults={"is_center_manager": False}
        )

        if user.is_center_manager:
            return Response({"error": "Use manager login"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "success": True,
                "created": created,
                "is_center_manager": False,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=200,
        )


class ManagerLoginTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
        if not phone:
            return Response({"error": "Phone required"}, status=400)

        user, created = User.objects.get_or_create(phone=phone)
        user.is_center_manager = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "success": True,
                "created": created,
                "is_center_manager": True,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=200,
        )


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "token_type": "Bearer",
                },
                status=200,
            )
        except Exception:
            return Response({"error": "Invalid token"}, status=401)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        return Response({"success": True, "message": "Logged out"}, status=200)
