from django.urls import path
from .views import CustomAuthToken, LogoutView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
