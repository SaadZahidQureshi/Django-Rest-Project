from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Team
from .serializers import TeamSerializer
from api.core.permissions import IsAdmin, IsManager, IsUser
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return Team.objects.all()
        elif user.role == User.Role.MANAGER:
            return Team.objects.filter(manager=user)
        return Team.objects.filter(members=user)
