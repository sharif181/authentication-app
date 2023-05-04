from django.urls import path, include

from .views import (
    RegisterView,
    UserListView,
    activateView,
    TokenObtainPairViewOverwrite
)

app_name = 'users'

urlpatterns = [
    path('token/', TokenObtainPairViewOverwrite.as_view()),
    path('register/', RegisterView.as_view()),
    path('user-list/', UserListView.as_view()),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activateView,
         name='activate'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
