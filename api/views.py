import decimal
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    DashboardSerializer,
    TransactionRecordSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    ServiceSerializer,
    ChangePasswordSerializer,
    VerifyAccountSerializer,
    MetaTagsSerializer,
    ResendOTPSerializer,
)
from accounts.models import Account, Profile
from app.models import Dashboard, TransactionRecord, Service, MetaTags
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from django.contrib.auth.password_validation import (
    validate_password,
)
from django.core.exceptions import ValidationError

from .email import send_otp_via_email

User = get_user_model()


class CustomUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# api to CRUD meta tags
class MetaTagsView(ModelViewSet):
    serializer_class = MetaTagsSerializer
    permission_classes = [IsAdminUser]
    queryset = MetaTags.objects.all()


class ReferralView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, ref_code):
        serializer = RegisterSerializer(data=request.data)
        password1 = request.data["password"]
        password2 = request.data["password2"]
        username = request.data["username"]
        email = request.data["email"]
        if serializer.is_valid():
            user = User(email=email, username=username)
            try:
                validate_password(password1, user)
            except ValidationError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            if password1 == password2:
                user.set_password(password1)
                user.save()
                send_otp_via_email(email, username)
                try:
                    referer = Profile.objects.get(referal_code=ref_code)
                except Profile.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                user.userprofile.refered_by = referer.user
                user.userprofile.save()
            else:
                return Response(
                    {"issue": "Passwords don't match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterSerializer(data=request.data)
        password = request.data["password"]
        password2 = request.data["password2"]
        email = request.data["email"]
        username = request.data["username"]
        if reg_serializer.is_valid():
            user = User(email=email, username=username)
            try:
                validate_password(password, user)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            if password == password2:
                user.set_password(password)
                user.save()
                send_otp_via_email(email, username)
            else:
                return Response(
                    {"issue": "Passwords don't match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(reg_serializer.data, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password hashes the new password that the user will provide
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        email = request.data["email"]
        otp = request.data["otp"]
        if serializer.is_valid():
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if not user.is_verified:
                if user.otp == otp:
                    user.is_verified = True
                    user.save()
                    return Response(
                        {"data": "account verified"},
                        status=status.HTTP_202_ACCEPTED,
                    )
                return Response(
                    {"data": "invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"data": "user is verified"}, status=status.HTTP_304_NOT_MODIFIED
            )
        else:
            return Response(
                {"data": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResendOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        email = request.data["email"]
        if serializer.is_valid():
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            send_otp_via_email(email, user.username)
            return Response({"data": "new OTP sent"}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": str(e)})


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = request.user.id
        try:
            Account.objects.get(id=user_id).delete()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_dashboard = Dashboard.objects.get(user=request.user)
        serializer = DashboardSerializer(user_dashboard)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_transaction = TransactionRecord.objects.filter(
                Q(sender=request.user) | Q(receiver=request.user)
            ).order_by("-timestamp")
        except TransactionRecord.DoesNotExist:
            return Response(
                {"detail": "This user has no transaction"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TransactionRecordSerializer(user_transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransferWithEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        amount = data["amount"]
        transfer_note = data["transfer_note"]
        try:
            receiver = Account.objects.get(email=data["email"])
        except Account.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        """
        service charge has not been added to the transaction
        service charge needs to be in sender balance also before transaction is allowed
        """
        if user.userdashboard.wallet_balance > decimal.Decimal(amount):
            user.userdashboard.wallet_balance -= decimal.Decimal(amount)
            user.userdashboard.save()

            receiver.userdashboard.wallet_balance += decimal.Decimal(amount)
            receiver.userdashboard.save()
            try:
                TransactionRecord.objects.create(
                    sender=user,
                    receiver=receiver,
                    amount=str(amount),
                    transaction_remark=transfer_note,
                )
                return Response(
                    {"success": "transfer successful!", "status": status.HTTP_200_OK}
                )
            except Exception as e:
                return Response(
                    {"error": str(e) + "Transaction record was not created!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response("Insufficient funds", status=status.HTTP_406_NOT_ACCEPTABLE)


class TransferWithTagView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        sender = request.user
        amount = data["amount"]
        transfer_note = data["transfer_note"]

        try:
            receiver = Dashboard.objects.get(wallet_tag=data["tag"])
        except Dashboard.DoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        if sender.userdashboard.wallet_balance > decimal.Decimal(amount):
            sender.userdashboard.wallet_balance -= decimal.Decimal(amount)
            sender.userdashboard.save()

            receiver.wallet_balance += decimal.Decimal(amount)
            receiver.save()

            TransactionRecord.objects.create(
                sender=sender,
                receiver=receiver.user,
                amount=str(amount),
                transaction_remark=transfer_note,
            )
            return Response("success", status=status.HTTP_200_OK)
        return Response(
            {"error": "Insufficient funds"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )


# class ServiceView(ModelViewSet):
#     permission_classes = [CustomUserPermission]
#     serializer_class = ServiceSerializer
#     queryset = Service.objects.all()

#     def get_object(self, *args, **kwargs):
#         id = self.kwargs.get("id")
#         try:
#             Service.objects.get(id=id)
#         except Service.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)


# class FindServiceView(APIView):
#     def get(self, request):
#         city = request.data["city"]
#         category = request.data["category"]

#         try:
#             services = Service.objects.filter(
#                 Q(city__icontains=city) | Q(category__category__icontains=category)
#             )
#         except Service.DoesNotExist:
#             return Response(
#                 {"error": "the service, city or the category is non-existent!"}
#             )
#         serializer = ServiceSerializer(services, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
