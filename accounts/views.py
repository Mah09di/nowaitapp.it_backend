<<<<<<< HEAD
import logging
=======
>>>>>>> develop
import secrets
from datetime import timedelta
import requests
from django.utils import timezone
from django.conf import settings
<<<<<<< HEAD
from django.core.cache import cache
=======
>>>>>>> develop
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, ManagerOTP
from core.models import Center

# ============================================================
# 📱 SMS PROVIDER CONFIGURATION
# ============================================================

<<<<<<< HEAD
# Security Constants
MAX_OTP_ATTEMPTS = 3
OTP_LOCKOUT_TIME = 300
TOKEN_EXPIRY_DAYS = 1
REFRESH_TOKEN_EXPIRY_DAYS = 7

# Ghasedak Settings
=======
>>>>>>> develop
GHASEDAK_API_KEY = "P/gEN/k+t6qVTLRd1Fzede42XCe+wJjYkGsLKx2ZaGM"
GHASEDAK_URLS = [
    "https://api.ghasedaksms.com/v2/send/verify",
    "https://rest.ghasedaksms.com/v2/send/verify",
<<<<<<< HEAD
]


def _issue_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.set_exp(lifetime=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS))
    refresh.access_token.set_exp(lifetime=timedelta(days=TOKEN_EXPIRY_DAYS))
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "expires_in": TOKEN_EXPIRY_DAYS * 24 * 3600,
        "token_type": "Bearer",
    }


=======
    "http://api.ghasedaksms.com/v2/send/verify",
    "https://gateway.ghasedak.me/rest/api/v1/send/verify",
    "https://rest.ghasedak.me/v2/send/verify",
]


>>>>>>> develop
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


<<<<<<< HEAD
def validate_phone(phone):
    import re

    pattern = r"^09[0-9]{9}$"
    return bool(re.match(pattern, phone))


def _send_otp_via_sms(phone, code):
=======
def send_sms_via_ghasedak(phone, otp_code):
>>>>>>> develop
    payload = {
        "receptor": phone,
        "type": 1,
        "template": "AuthCode",
<<<<<<< HEAD
        "param1": str(code),
=======
        "param1": str(otp_code),
>>>>>>> develop
    }
    headers = {
        "apikey": GHASEDAK_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    for url in GHASEDAK_URLS:
        try:
<<<<<<< HEAD
            response = requests.post(url, data=payload, headers=headers, timeout=5)
            if response.status_code in (200, 201, 202):
                return True, "SMS sent successfully"
        except Exception:
            continue

    return False, "All SMS providers failed"
=======
            print(f"📤 Attempting: {url}")
            response = requests.post(url, data=payload, headers=headers, timeout=8)
            print(f"📥 Status: {response.status_code}")

            if response.status_code in (200, 201, 202):
                return True, "SMS sent successfully", url
        except Exception:
            continue

    return False, "All SMS providers failed", None


# ============================================================
# 🔐 AUTHENTICATION APIS
# ============================================================
>>>>>>> develop


class ManagerLoginStartView(APIView):
    """
    Step 1: Check if user exists and send OTP
    - If user exists: sends OTP for login
    - If user doesn't exist: returns status for registration
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="manager_login_start",
        operation_description=(
            "🔐 **Step 1 - Check User & Send OTP**\n\n"
            "Check if phone number is registered.\n\n"
            "**Flow:**\n"
            "1. User enters phone number\n"
            "2. System checks if user exists\n"
            "3. If exists: sends OTP for login\n"
            "4. If not exists: returns registration required status"
        ),
        operation_summary="📱 Check User & Send OTP",
        tags=["🔐 Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone"],
            properties={
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="📞 Iranian phone number (format: 09123456789)",
                    example="09123456789",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="✅ OTP Sent (User exists)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="OTP sent successfully",
                        ),
                        "user_exists": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            example=True,
                        ),
                    },
                ),
            ),
            202: openapi.Response(
                description="📝 Registration Required (User not found)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User not found. Please register.",
                        ),
                        "user_exists": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            example=False,
                        ),
                        "requires_registration": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            example=True,
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="❌ Bad Request",
            ),
            429: openapi.Response(
                description="⏱️ Too Many Requests",
            ),
        },
    )
    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
<<<<<<< HEAD

        if not phone or not validate_phone(phone):
            return Response(
                {"error": "INVALID_PHONE", "message": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lockout_key = f"otp_lockout_{phone}"
        if cache.get(lockout_key):
            return Response(
                {"error": "TOO_MANY_ATTEMPTS", "message": "Too many attempts"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        user, _ = User.objects.get_or_create(phone=phone)
        otp_code = f"{secrets.randbelow(900000) + 100000}"

        otp_obj, _ = ManagerOTP.objects.get_or_create(phone=phone)
        otp_obj.touch_new_code(code=otp_code, ttl_seconds=300)

        sms_sent, _ = _send_otp_via_sms(phone, otp_code)

        if settings.DEBUG:
            print(f"\n{'='*60}")
            print(f"OTP for {phone}: {otp_code}")
            print(f"{'='*60}\n")

        if sms_sent:
            return Response(
                {"message": "OTP sent successfully"}, status=status.HTTP_200_OK
            )
        else:
            attempt_key = f"otp_attempts_{phone}"
            attempts = cache.get(attempt_key, 0) + 1
            cache.set(attempt_key, attempts, timeout=300)

            if attempts >= MAX_OTP_ATTEMPTS:
                cache.set(lockout_key, True, timeout=OTP_LOCKOUT_TIME)

            return Response(
                {"error": "SMS_FAILED", "message": "Failed to send SMS"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
=======
        if not phone:
            return Response({"error": "Phone required"}, status=400)

        try:
            user = User.objects.get(phone=phone)
            user_exists = True
        except User.DoesNotExist:
            user_exists = False

        if user_exists:
            otp_code = f"{secrets.randbelow(900000) + 100000}"
            otp_obj, _ = ManagerOTP.objects.get_or_create(phone=phone)
            otp_obj.touch_new_code(code=otp_code, ttl_seconds=300)

            print(f"\n{'='*60}")
            print(f"📱 OTP for {phone}: {otp_code}")
            print(f"👤 Existing user: {phone}")
            print(f"{'='*60}\n")

            sms_sent, sms_message, used_url = send_sms_via_ghasedak(phone, otp_code)

            if sms_sent:
                return Response(
                    {
                        "message": "OTP sent successfully",
                        "user_exists": True,
                    },
                    status=200,
                )
            else:
                return Response(
                    {
                        "message": "OTP generated (SMS failed - check console)",
                        "code": otp_code if settings.DEBUG else None,
                        "user_exists": True,
                        "sms_error": sms_message,
                    },
                    status=200,
                )

        return Response(
            {
                "message": "User not found. Please register.",
                "user_exists": False,
                "requires_registration": True,
            },
            status=202,
        )


class ManagerRegisterView(APIView):
    """
    Step 2: Register new user with center info and location
    - Creates user and center with location coordinates
    - Sends OTP after registration
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="manager_register",
        operation_description=(
            "📝 **Register New Manager**\n\n"
            "Register a new manager with center information and location.\n\n"
            "**Fields:**\n"
            "- `phone`: Iranian phone number (required)\n"
            "- `center_name`: Name of the center (required)\n"
            "- `latitude`: GPS latitude (required)\n"
            "- `longitude`: GPS longitude (required)\n"
            "- `address`: Full address (optional)\n\n"
            "**Flow:**\n"
            "1. User enters phone, center name, and location\n"
            "2. System creates user and center\n"
            "3. OTP sent to phone\n"
            "4. User can now login"
        ),
        operation_summary="📝 Register New Manager",
        tags=["🔐 Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone", "center_name", "latitude", "longitude"],
            properties={
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="📞 Iranian phone number",
                    example="09123456789",
                ),
                "center_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="🏢 Center name",
                    example="آرایشگاه ستاره",
                ),
                "latitude": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="🌐 GPS Latitude (e.g., 35.6892)",
                    example=35.6892,
                ),
                "longitude": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="🌐 GPS Longitude (e.g., 51.3890)",
                    example=51.3890,
                ),
                "address": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="📍 Full address (optional)",
                    example="تهران، خیابان آزادی، پلاک ۱۲۳",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="✅ Registration successful, OTP sent",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User registered successfully. OTP sent.",
                        ),
                        "user_exists": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            example=True,
                        ),
                        "requires_registration": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            example=False,
                        ),
                        "center": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "latitude": openapi.Schema(type=openapi.TYPE_NUMBER),
                                "longitude": openapi.Schema(type=openapi.TYPE_NUMBER),
                                "address": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="❌ Bad Request",
            ),
        },
    )
    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
        center_name = request.data.get("center_name")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        address = request.data.get("address", "")

        # ============================================================
        # 🔍 Validation
        # ============================================================
        if not phone or not center_name:
            return Response(
                {
                    "error": "Phone and center_name are required",
                },
                status=400,
            )

        if latitude is None or longitude is None:
            return Response(
                {
                    "error": "Latitude and longitude are required",
                },
                status=400,
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return Response(
                {"error": "Latitude and longitude must be valid numbers"},
                status=400,
            )

        # ============================================================
        # 🔍 Check if user already exists
        # ============================================================
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"is_center_manager": False},
        )

        if not created:
            return Response(
                {
                    "error": "User already exists. Please login.",
                    "user_exists": True,
                },
                status=400,
            )

        # ============================================================
        # 🏢 Create center for user with location
        # ============================================================
        center = Center.objects.create(
            user=user,
            name=center_name,
            address=address,
            phone=phone,
            latitude=latitude,
            longitude=longitude,
        )

        print(f"\n{'='*60}")
        print(f"🆕 New user registered: {phone}")
        print(f"🏢 Center created: {center_name}")
        print(f"📍 Address: {address}")
        print(f"🌐 Location: {latitude}, {longitude}")
        print(f"{'='*60}\n")

        # ============================================================
        # 🔐 Generate and send OTP
        # ============================================================
        otp_code = f"{secrets.randbelow(900000) + 100000}"
        otp_obj, _ = ManagerOTP.objects.get_or_create(phone=phone)
        otp_obj.touch_new_code(code=otp_code, ttl_seconds=300)

        print(f"📱 OTP for {phone}: {otp_code}")

        sms_sent, sms_message, used_url = send_sms_via_ghasedak(phone, otp_code)

        response_data = {
            "message": (
                "User registered successfully. OTP sent."
                if sms_sent
                else "User registered. OTP generated (SMS failed)."
            ),
            "user_exists": True,
            "requires_registration": False,
            "center": {
                "name": center.name,
                "latitude": center.latitude,
                "longitude": center.longitude,
                "address": center.address,
            },
        }

        if not sms_sent and settings.DEBUG:
            response_data["code"] = otp_code
            response_data["sms_error"] = sms_message

        return Response(response_data, status=200)
>>>>>>> develop


class ManagerVerifyView(APIView):
    """
    Step 3: Verify OTP Code - Returns JWT tokens on success
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="manager_login_verify_otp",
        operation_description=(
            "🔐 **Step 3 - Verify OTP & Login**\n\n"
            "Confirm the OTP code received via SMS and receive JWT tokens.\n\n"
            "**Flow:**\n"
            "1. User enters phone number and OTP code\n"
            "2. System validates the code (5 min expiry, 3 attempts max)\n"
            "3. On success: JWT tokens issued\n"
            "4. Account becomes manager\n\n"
            "**Tokens:**\n"
            "- `access`: Valid for 24 hours\n"
            "- `refresh`: Valid for 7 days"
        ),
        operation_summary="🔑 Verify OTP & Login",
        tags=["🔐 Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone", "code"],
            properties={
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="📞 Phone number used in step 1",
                    example="09123456789",
                ),
                "code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="🔢 6-digit OTP code received via SMS",
                    example="123456",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="✅ Login Successful",
            ),
            400: openapi.Response(
                description="❌ Invalid Request",
            ),
        },
    )
    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
        code = request.data.get("code")

<<<<<<< HEAD
        if not phone or not validate_phone(phone) or not code:
            return Response(
                {"error": "INVALID_REQUEST", "message": "Phone and code are required"},
                status=status.HTTP_400_BAD_REQUEST,
=======
        if not phone or not code:
            return Response(
                {"error": "INVALID_REQUEST", "message": "Phone and code are required"},
                status=400,
>>>>>>> develop
            )

        try:
            otp_obj = ManagerOTP.objects.get(phone=phone)
        except ManagerOTP.DoesNotExist:
            return Response(
                {"error": "OTP_NOT_FOUND", "message": "OTP not found or expired"},
<<<<<<< HEAD
                status=status.HTTP_400_BAD_REQUEST,
=======
                status=400,
>>>>>>> develop
            )

        if otp_obj.is_expired():
            otp_obj.delete()
            return Response(
                {"error": "OTP_EXPIRED", "message": "OTP has expired"},
<<<<<<< HEAD
                status=status.HTTP_400_BAD_REQUEST,
=======
                status=400,
>>>>>>> develop
            )

        if str(otp_obj.code) != str(code):
            otp_obj.increment_attempts()
<<<<<<< HEAD
            remaining_attempts = MAX_OTP_ATTEMPTS - otp_obj.attempts

            if otp_obj.attempts >= MAX_OTP_ATTEMPTS:
                otp_obj.delete()
                return Response(
                    {
                        "error": "MAX_ATTEMPTS_EXCEEDED",
                        "message": "Maximum attempts exceeded",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {
                    "error": "INVALID_CODE",
                    "message": f"Invalid code. {remaining_attempts} attempts remaining",
                },
                status=status.HTTP_400_BAD_REQUEST,
=======
            remaining = 3 - otp_obj.attempts
            return Response(
                {
                    "error": "INVALID_CODE",
                    "message": f"Invalid code. {remaining} attempts remaining",
                },
                status=400,
>>>>>>> develop
            )

        otp_obj.delete()
        user, created = User.objects.get_or_create(phone=phone)
<<<<<<< HEAD
=======

        is_new_user = created

>>>>>>> develop
        user.is_center_manager = True
        user.last_login = timezone.now()
        user.save(update_fields=["is_center_manager", "last_login"])

<<<<<<< HEAD
        tokens = _issue_tokens_for_user(user)

        return Response(
            {"success": True, "is_center_manager": True, **tokens},
            status=status.HTTP_200_OK,
=======
        refresh = RefreshToken.for_user(user)

        print(f"✅ Manager login successful: {phone} (New user: {is_new_user})")

        return Response(
            {
                "success": True,
                "is_center_manager": True,
                "is_new_user": is_new_user,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "expires_in": 24 * 3600,
                "token_type": "Bearer",
            },
            status=200,
>>>>>>> develop
        )


class VisitorLoginView(APIView):
    """Visitor login without OTP - Simple phone number login"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="visitor_login",
        operation_description=(
            "👤 **Visitor Login (No OTP Required)**\n\n"
            "Simple login for visitors/customers.\n\n"
            "**Note:** Cannot be used for manager accounts"
        ),
        operation_summary="👤 Visitor Login",
        tags=["🔐 Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone"],
            properties={
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="📞 Iranian phone number",
                    example="09123456789",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="✅ Login Successful",
            ),
            400: openapi.Response(
                description="❌ Invalid Request",
            ),
        },
    )
    def post(self, request):
        phone = normalize_phone(request.data.get("phone"))
<<<<<<< HEAD

        if not phone or not validate_phone(phone):
            return Response(
                {"error": "INVALID_PHONE", "message": "Invalid phone number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            phone=phone, defaults={"is_center_manager": False}
        )

        if user.is_center_manager:
            return Response(
                {"error": "ACCOUNT_TYPE_MISMATCH", "message": "Use manager login"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        tokens = _issue_tokens_for_user(user)

        return Response(
            {"success": True, "created": created, "is_center_manager": False, **tokens},
            status=status.HTTP_200_OK,
        )


class ManagerLoginTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.DEBUG:
            return Response(
                {"error": "FORBIDDEN", "message": "Test login only in debug mode"},
                status=status.HTTP_403_FORBIDDEN,
            )

        phone = normalize_phone(request.data.get("phone"))
        if not phone or not validate_phone(phone):
            return Response(
                {"error": "INVALID_PHONE", "message": "Invalid phone number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(phone=phone)
        user.is_center_manager = True
        user.last_login = timezone.now()
        user.save(update_fields=["is_center_manager", "last_login"])

        tokens = _issue_tokens_for_user(user)

        return Response(
            {"success": True, "created": created, "is_center_manager": True, **tokens},
            status=status.HTTP_200_OK,
=======
        if not phone:
            return Response({"error": "Phone required"}, status=400)

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"is_center_manager": False},
        )

        if user.is_center_manager:
            return Response(
                {"error": "ACCOUNT_TYPE_MISMATCH", "message": "Use manager login"},
                status=400,
            )

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

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
>>>>>>> develop
        )


class TokenRefreshView(APIView):
<<<<<<< HEAD
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

=======
    """Refresh expired access token using refresh token"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="refresh_token",
        operation_description=(
            "🔄 **Refresh Access Token**\n\n"
            "Use refresh token to get a new access token when expired.\n\n"
            "**Token Lifetimes:**\n"
            "- Access Token: 24 hours\n"
            "- Refresh Token: 7 days"
        ),
        operation_summary="🔄 Refresh Token",
        tags=["🔐 Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="🔑 Refresh token from login response",
                    example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="✅ New Access Token Generated",
            ),
            400: openapi.Response(description="❌ Refresh token required"),
            401: openapi.Response(description="❌ Invalid or expired refresh token"),
        },
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
>>>>>>> develop
        if not refresh_token:
            return Response(
                {
                    "error": "REFRESH_TOKEN_REQUIRED",
                    "message": "Refresh token is required",
                },
<<<<<<< HEAD
                status=status.HTTP_400_BAD_REQUEST,
=======
                status=400,
>>>>>>> develop
            )

        try:
            refresh = RefreshToken(refresh_token)
<<<<<<< HEAD
            access_token = str(refresh.access_token)
            return Response(
                {
                    "access": access_token,
                    "expires_in": TOKEN_EXPIRY_DAYS * 24 * 3600,
                    "token_type": "Bearer",
                },
                status=status.HTTP_200_OK,
=======
            return Response(
                {
                    "access": str(refresh.access_token),
                    "token_type": "Bearer",
                },
                status=200,
>>>>>>> develop
            )
        except Exception:
            return Response(
                {
                    "error": "INVALID_TOKEN",
                    "message": "Invalid or expired refresh token",
                },
<<<<<<< HEAD
                status=status.HTTP_401_UNAUTHORIZED,
=======
                status=401,
>>>>>>> develop
            )


class LogoutView(APIView):
<<<<<<< HEAD
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

=======
    """Logout user by blacklisting refresh token"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="logout",
        operation_description=(
            "🚪 **Logout**\n\n"
            "Blacklist the refresh token to complete logout.\n"
            "Access token will automatically expire after 24 hours."
        ),
        operation_summary="🚪 Logout",
        tags=["🔐 Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="🔑 Refresh token to blacklist",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="✅ Logged out successfully",
            ),
        },
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
>>>>>>> develop
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
<<<<<<< HEAD

        return Response(
            {"success": True, "message": "Logged out successfully"},
            status=status.HTTP_200_OK,
        )
=======
        return Response(
            {"success": True, "message": "Logged out successfully"},
            status=200,
        )
    
>>>>>>> develop
