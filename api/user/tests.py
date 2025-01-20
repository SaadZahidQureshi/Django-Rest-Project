# api/user/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from api.team.models import Team
from api.core.choices import Roles

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_obtain_jwt_token(self):
        # Using username and password for token generation
        response = self.client.post('/api/token/', {
            'username': self.user_data['username'],  # Changed from email to username
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        # First obtain tokens using username/password
        response = self.client.post('/api/token/', {
            'username': self.user_data['username'],  # Changed from email to username
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']
        
        # Then try to refresh
        response = self.client.post('/api/token/refresh/', {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class AdminViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role=Roles.ADMIN
        )
        # Create some regular users for testing
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123',
            role=Roles.USER
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123',
            role=Roles.USER
        )

    def test_admin_can_list_all_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/admin/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # admin + 2 users

    def test_non_admin_cannot_access_admin_view(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/admin/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ManagerViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='manager123',
            role=Roles.MANAGER
        )
        self.team_member1 = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='pass123',
            role=Roles.USER
        )
        self.team_member2 = User.objects.create_user(
            username='member2',
            email='member2@example.com',
            password='pass123',
            role=Roles.USER
        )
        self.non_team_member = User.objects.create_user(
            username='nonmember',
            email='nonmember@example.com',
            password='pass123',
            role=Roles.USER
        )
        # Create team and add members
        self.team = Team.objects.create(name='Test Team', manager=self.manager)
        self.team.members.add(self.team_member1, self.team_member2)

    def test_manager_can_view_team_members(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get('/api/manager/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only team members

    def test_manager_can_update_team_member_role(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.put(
            '/api/manager/',  # Changed URL to match your urls.py
            {
                'user_id': self.team_member1.id,  # Added user_id in request data
                'role': Roles.MANAGER
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team_member1.refresh_from_db()
        self.assertEqual(self.team_member1.role, Roles.MANAGER)

    def test_manager_cannot_update_non_team_member(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.put(
            '/api/manager/',  # Changed URL to match your urls.py
            {
                'user_id': self.non_team_member.id,
                'role': Roles.MANAGER
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='pass123',
            role=Roles.USER
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='pass123',
            role=Roles.USER
        )

    def test_user_can_view_own_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_can_update_own_profile(self):
        self.client.force_authenticate(user=self.user)
        new_username = 'updated_username'
        response = self.client.put(
            '/api/user/',
            {'username': new_username}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_username)

    def test_user_cannot_access_other_profiles(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/user/{self.other_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)