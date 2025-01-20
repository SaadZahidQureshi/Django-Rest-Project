from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UpdateUserRoleSerializer, UpdateUserProfileSerializer
from api.core.permissions import IsAdmin, IsManager, IsUser

User = get_user_model()


class AdminView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManagerView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        team_members = User.objects.filter(teams__manager=request.user).distinct()
        serializer = UserSerializer(team_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk, teams__manager=request.user)
        except User.DoesNotExist:
            return Response({'error': 'User not found or not part of your team'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserRoleSerializer(data=request.data)
        if serializer.is_valid():
            user.role = serializer.validated_data['role']
            user.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UpdateUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            request.user.username = serializer.validated_data['username']
            request.user.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)