from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Session, Account, Computer
from ..serializers import SessionSerializer

class SessionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.session_url = reverse('session-list')
        self.create_session_url = reverse('session-create-session')
        self.account = Account.objects.create(username='testuser')
        self.computer = Computer.objects.create(name='Test Computer')

    def test_get_session_list(self):
        response = self.client.get(self.session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_session(self):
        self.client.force_login(self.account)
        data = {'computer': self.computer.id}
        response = self.client.post(self.create_session_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_invalid_computer(self):
        self.client.force_login(self.account)
        data = {'computer': 999}  # Invalid computer ID
        response = self.client.post(self.create_session_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_session(self):
        session = Session.objects.create(account=self.account, computer=self.computer)
        end_session_url = reverse('session-end-session', kwargs={'pk': session.id})
        response = self.client.put(end_session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        session.refresh_from_db()
        self.assertIsNotNone(session.end_time)

    def test_get_my_all_session(self):
        self.client.force_login(self.account)
        response = self.client.get(reverse('session-my-all-session'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_my_session(self):
        self.client.force_login(self.account)
        response = self.client.get(reverse('session-my-session'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Assuming user doesn't have a session
