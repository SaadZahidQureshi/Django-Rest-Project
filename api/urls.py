
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.user.views import UserView, ManagerView, AdminView
from api.team.views import TeamViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"team", TeamViewSet, basename="team")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('admin/', AdminView.as_view(), name='admin-view'),
    path('manager/<int:pk>/', ManagerView.as_view(), name='manager-update-view'),
    path('manager/', ManagerView.as_view(), name='manager-view'),
    path('user/', UserView.as_view(), name='user-view'),
] + router.urls
