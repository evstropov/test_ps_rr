from django.urls import path

from organization.views import organization_balance

urlpatterns = [
    path('<int:inn>/balance/', organization_balance),
]
