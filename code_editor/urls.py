from django.urls import path
from .views import RunCodeView

urlpatterns = [
    path('code/', RunCodeView.as_view(), name='run-code'),
]
