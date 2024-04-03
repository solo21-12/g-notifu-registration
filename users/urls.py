from django.urls import path
from .views import (
    CompanyOwnerUpdateDeleteView,
    CompanyOwnerCreateView,
    IndvidualOwnerCreateView,
    IndvidualOwnerUpdateDeleteView,
    UserEmailVerificationView,
    UserPasswordResetRequestView,
    UserPasswordResetView,
    UserPasswordSetView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('in/create', IndvidualOwnerCreateView,
                basename='indvidual-create')
router.register('in/update', IndvidualOwnerUpdateDeleteView,
                basename='indvidual-update')
router.register('co/create', CompanyOwnerCreateView, basename='company-create')
router.register('co/update', CompanyOwnerUpdateDeleteView,
                basename='company-update')

urlpatterns = [
    path('verify-email/', UserEmailVerificationView.as_view(), name='verify_email'),
    path("reset-password-request/",
         UserPasswordResetRequestView.as_view(), name="reset password"),
    path("reset-password-change/", UserPasswordResetView.as_view(),
         name="reset password update"),
    path("set-up-password", UserPasswordSetView.as_view(), name="set_up_password")

] + router.urls
