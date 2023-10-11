from django.urls import path
from .views import OnboardTextByTypeView

urlpatterns = [
    path(
        "<slug:onboarding_type_slug>",
        OnboardTextByTypeView.as_view(),
        name="onboarding-by-type",
    ),
]
