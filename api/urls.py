from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardView,
    TransactionsView,
    # TransferView,
    TransferWithEmailView,
    TransferWithTagView,
    ServiceView,
    # ServiceDetailView,
    # ServiceUpdateDeleteView,
    LogoutView,
    DeleteAccountView,
    FindServiceView,
    ChangePasswordView,
    ReferralView,
    VerifyOTP,
    ResendOTP,
    MetaTagsView,
    RegView,
)

router = DefaultRouter()
router.register("metatag", MetaTagsView, basename="app_metatags")
router.register("service", ServiceView, basename="service")

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("referal/<str:ref_code>/", ReferralView.as_view(), name="referal"),
    path("verify-otp/", VerifyOTP.as_view(), name="verifyotp"),
    path("resend-otp/", ResendOTP.as_view(), name="resendotp"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("register/", RegView.as_view(), name="apiregister"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete_account"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("transactions/", TransactionsView.as_view(), name="transactions"),
    path("transfer/email/", TransferWithEmailView.as_view(), name="email_transfer"),
    path("transfer/tag/", TransferWithTagView.as_view(), name="tag_transfer"),
    path("search/", FindServiceView.as_view(), name="search"),
    path("", include(router.urls)),
]
